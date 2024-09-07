# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class ReturnOrderLine(models.TransientModel):
    _name = 'return.order.line'
    _description = 'Return Order Line'

    return_id = fields.Many2one(string='return order', comodel_name='return.order')
    rma_line_id = fields.Many2one('rma.lines', 'RMA Line Id')
    product_id = fields.Many2one('product.product', 'Product')
    delivery_qty = fields.Float('Delivered Quantity')
    return_qty = fields.Float('Return/Cancel Quantity')
    recieved_qty = fields.Float('Recieved Quantity')
    sale_line_id = fields.Many2one(string='Order Line', comodel_name='sale.order.line')
    is_new_line = fields.Boolean('new line', default=False)
    pending_qty = fields.Float('Pending Quantity')
    rma_reason_id = fields.Many2one('rma.reason', 'Return/NoReturn')
    reject_reason_id = fields.Many2one('reject.reason', 'Reject Reason')
    tracking = fields.Selection(related='product_id.tracking')


    @api.onchange('return_qty')
    def _onchange_return_qty(self):
        self.update({
            'is_new_line': True})


class RmaReplaceOrderTran(models.TransientModel):
    _name = 'return.replace.order'
    _description = 'Return Replace Order'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    detailed_type = fields.Selection(related='product_id.detailed_type')
    qty = fields.Integer('Quantity', default=0)
    rma_id = fields.Many2one('return.order', string='RMA Order')
    is_new_line = fields.Boolean('new line', default=False)
    product_price = fields.Float(string="Product Price", default=0.0)

    @api.onchange('product_id', 'qty')
    def _onchange_for_new_line(self):
        self.update({
            'is_new_line': True})

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for prod in self:
            prod.product_price = prod.product_id.lst_price

            if prod.product_id and (prod.product_id.detailed_type == 'service'):
                prod.qty = 1


class ReturnOrder(models.TransientModel):
    _name = 'return.order'
    _description = 'Return Order'

    rma_order_id = fields.Many2one('rma.main', string='rma_order')
    rol_ids = fields.One2many(string='return order line', comodel_name='return.order.line', inverse_name='return_id')
    replace_prd_ids = fields.One2many(comodel_name='return.replace.order', inverse_name='rma_id', string='replace_prd')
    is_service = fields.Boolean(compute='_compute_is_service', string='is delivery', default=False)
    is_without_do_rma = fields.Boolean('Is without do rma')
    rma_type = fields.Selection([('rma_with_do', 'With DO')])

    @api.onchange("replace_prd_ids")
    @api.depends('replace_prd_ids.product_id', 'replace_prd_ids.qty')
    def _compute_is_service(self):
        for rplc_id in self:
            replace_prd_id = rplc_id.replace_prd_ids.filtered(lambda t: t.product_id.detailed_type == 'service')
            if replace_prd_id:
                rplc_id.is_service = True
            else:
                rplc_id.is_service = False

    @api.model
    def default_get(self, fields):
        res = super(ReturnOrder, self).default_get(fields)
        if self._context.get('default_rma_line', False):
            return_order_line_list = []
            rma_lines = self.env['rma.lines'].browse(self._context.get('default_rma_line', []))
            for i in rma_lines.filtered(lambda t: t.product_id.detailed_type != 'service'):
                vals ={
                    'rma_line_id': i.id,
                    'product_id': i.product_id.id,
                    'delivery_qty': i.delivery_qty,
                    'pending_qty': i.sale_line_id.product_uom_qty - i.sale_line_id.qty_delivered ,
                    'return_qty': i.return_qty,
                    'rma_reason_id':i.rma_reason_id.id,
                    'reject_reason_id': i.reject_reason_id.id,
                    }

                retun_vals = (0, 0,vals )
                return_order_line_list.append(retun_vals)
            if return_order_line_list != []:
                res.update({
                    'rol_ids': return_order_line_list,
                })
        replce_order_line_list = []
        if self._context.get('default_replace_prd_ids', []):

            rplc_lines = self.env['rma.replace.order'].browse(self._context.get('default_replace_prd_ids', []))
            for i in rplc_lines:
                rplcvals = (0, 0, {
                    'product_id': i.product_id.id,
                    'qty': i.qty,
                    'product_price': i.product_price
                })
                replce_order_line_list.append(rplcvals)
        if replce_order_line_list != []:
            res.update({
                'replace_prd_ids': replce_order_line_list,
            })
        res.update({
            'rma_order_id': self._context.get('default_rma_id'),
            'rma_type': self._context.get('default_rma_type'),
        })
        return res

    def check_basic_validation(self):
        if self.rol_ids.filtered(lambda t: t.rma_reason_id and not t.return_qty):
            raise ValidationError("Sorry! You have to enter return qty for all the RMA reason selected lines")
        if self.rol_ids.filtered(lambda t: not t.rma_reason_id and t.return_qty):
            raise ValidationError("Sorry! You have to select the return/no return for entered returned qty to proceed")
        if self.rol_ids.filtered(lambda t: t.rma_reason_id and not t.reject_reason_id):
            raise ValidationError("Sorry! You have to select reject reason to proceed")

    def update_rma_lines(self):
        if sum(self.rol_ids.filtered(lambda t: t.product_id.detailed_type != 'service').mapped('return_qty')) <= 0:
            raise ValidationError("Sorry! You have to enter at-lease one return item to proceed")
        if self.replace_prd_ids:
            if not sum(self.replace_prd_ids.mapped('qty')):
                raise ValidationError("Sorry! You have to enter at-lease one Quantity for replace product to proceed")
        if self.rma_type in ('rma_with_do'):
            self.check_basic_validation()
        for i in self.rol_ids:
            if i.is_new_line:
                if not i.rma_line_id.lot_ids:
                    other_rma_return_qty = sum(i.rma_line_id.sale_line_id.return_order_line_id.filtered(lambda x:x.rma_id and x.product_id.id == i.rma_line_id.product_id.id and x.rma_id.state not in ('reject', 'processing') and x.id != i.rma_line_id.id).mapped('return_qty'))
                else:
                    other_rma_return_qty = sum(i.rma_line_id.sale_line_id.return_order_line_id.filtered(lambda x: x.rma_id and x.product_id.id == i.rma_line_id.product_id.id and x.rma_id.state not in ('reject', 'processing') and x.id != i.rma_line_id.id and i.rma_line_id.lot_ids[0].id == x.lot_ids[0].id).mapped('return_qty'))
                if i.delivery_qty < i.rma_line_id.return_qty:
                    raise ValidationError('Return Quantity is more then Delivered quantity..!!')
                elif i.return_qty > i.delivery_qty:
                    raise ValidationError('Return Quantity should not be more then the delivered Qty.')
                elif i.return_qty > i.rma_line_id.sale_line_id.qty_delivered:
                    raise ValidationError('Return Quantity should not be more then the order delivered Qty.')
                elif other_rma_return_qty and i.delivery_qty < (other_rma_return_qty + i.return_qty):
                    raise ValidationError('Total return qty should not more then the order delivered qty')
                i.rma_line_id.return_qty = i.return_qty
            i.rma_line_id.rma_reason_id = i.rma_reason_id.id
            i.rma_line_id.reject_reason_id = i.reject_reason_id.id

        if self.replace_prd_ids:
            if len(self.replace_prd_ids.filtered(lambda x:x.qty <= 0)):
                raise ValidationError('Sorry!, We can not proceed with 0 qty, Please enter the quantity to proceed')

            rro_id = self.env['rma.replace.order'].search([('rma_id', '=', self.rma_order_id.id)])
            rro_id.unlink()
            for j in self.replace_prd_ids:
                total_price = j.product_id.lst_price * j.qty

                self.env['rma.replace.order'].create({
                    'rma_id': self.rma_order_id.id,
                    'product_id': j.product_id.id,
                    'qty': j.qty,
                    'product_price': j.product_price,
                    'total_price': total_price
                })
            self.rma_order_id._update_return_total()
