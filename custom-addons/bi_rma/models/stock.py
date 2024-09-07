from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
import base64
import requests
import json
from setuptools import Require

import logging

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.constrains('quantity')
    def check_quantity(self):
        for quant in self:
            if float_compare(quant.quantity, 1,
                             precision_rounding=quant.product_uom_id.rounding) > 0 and quant.lot_id and quant.product_id.tracking == 'serial':
                return


class StockMove(models.Model):
    _inherit = "stock.move"

    rma_line_id = fields.Many2one('rma.lines')

    @api.onchange('quantity')
    def _onchange_quantity_done(self):
        if self.picking_id and self.picking_id.rma_id:
            if self.quantity > self.product_uom_qty:
                raise UserError(_("You can't transfer more than the Initial Demand!"))


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    return_qty = fields.Integer(string="Return Qty")

    @api.onchange('lot_id')
    def validation_for_rma_stock_picking_lot_id(self):
        for stockmoveline in self:
            if stockmoveline.picking_id.rma_id and stockmoveline.picking_id.picking_type_id.id == stockmoveline.picking_id.picking_type_id.company_id.b2b_source_picking_type_id.id:
                raise ValidationError('Sorry!, You can not change the lot for the RMA Inwards')
            if stockmoveline.picking_id.rma_id and stockmoveline.picking_id.picking_type_id.id == stockmoveline.picking_id.picking_type_id.company_id.b2b_without_return_items_picking_type_id.id:
                raise ValidationError('You can not change the lot for the RMA Inwards.')

    @api.onchange('quantity')
    def _onchange_qty_done(self):
        if self.move_id and self.move_id.picking_id and self.move_id.picking_id.rma_id:
            if self.quantity > self.move_id.product_uom_qty:
                raise UserError(_("You can't transfer more than the Initial Demand!"))


class RmaStockPicking(models.Model):
    _inherit = "stock.picking"

    rma_id = fields.Many2one('rma.main', string='RMA ID')
    claim_id = fields.Many2one('rma.claim', string='Claim ID')
    claim_count = fields.Float('Claim Count ', compute='_compute_rma_claim_ids')
    replace_picking_out_rma_count = fields.Integer(compute='_replace_picking_out_rma_count')
    reason_action = fields.Selection([('refund_with_returned_item', 'Replace with Returned Items'),
                                      ('refund_without_returned_item', 'Replace with out Returned Items'),
                                      ], string='Action')

    def action_to_view_rma(self):
        self.ensure_one()
        rma_id = False

        if self.sale_id and self.sale_id.rma_id:
            rma_id = self.sale_id.rma_id
        if not rma_id and self.rma_id:
            rma_id = self.rma_id
        if rma_id:
            return {
                'name': 'RMA',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'rma.main',
                'domain': [('id', '=', rma_id.id)],
            }

    def _replace_picking_out_rma_count(self):
        for picking in self:
            picking.replace_picking_out_rma_count = 0
            if picking.sale_id and picking.sale_id.rma_id:
                picking.replace_picking_out_rma_count = 1
            if picking.rma_id:
                picking.replace_picking_out_rma_count = 1

    def _compute_rma_claim_ids(self):
        for order in self:
            rma_claim_ids = self.env['rma.claim'].search([('stock_picking_id', '=', order.id)])
            order.claim_count = len(rma_claim_ids)

    def action_rma_claim_view(self):
        self.ensure_one()
        return {
            'name': 'Rma Claim',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'rma.claim',
            'domain': [('stock_picking_id', '=', self.id)],
            'context': {
                'create': False,
            },
        }

    def button_validate(self):
        rma_claim_obj = self.env['rma.claim'].sudo()
        validate_super = super(RmaStockPicking, self).button_validate()

        rma_line_list = []
        move_line_list = []
        related_picking_rma = self.env['rma.main'].search([('id', '=', self.rma_id.id)])
        related_picking_rma.write({'state': 'processing'})

        for picking in self:
            if picking.picking_type_code == 'incoming' and picking.rma_id:
                for r in related_picking_rma.rma_line_ids:
                    rma_line_list.append(r.id)
                for m in picking.move_ids:
                    move_line_list.append(m.id)
                for i, j in zip(rma_line_list, move_line_list):
                    get_qty = self.env['stock.move'].browse(j)
                    self.env['rma.lines'].browse(i).write({'recieved_qty': get_qty.product_uom_qty})
                vals = {
                    'rma_id': picking.rma_id.id,
                    'subject': picking.rma_id.subject,
                    'partner': picking.rma_id.del_partner.id,
                    'responsible': picking.rma_id.responsible.id,
                    'date': picking.rma_id.date,
                    'nxt_act_dt': datetime.now(),
                    'nxt_act': datetime.now(),
                    'stock_picking_id': picking.rma_id.delivery_order.id
                }
                if not rma_claim_obj.search_count([('stock_picking_id', '=', picking.rma_id.delivery_order.id)]):
                    rma_claim_obj.create(vals)
                if picking.state == 'done':
                    invoice_ids = self.env['account.move'].search(
                        [('picking_id', '=', picking.rma_id.delivery_order.id), ('move_type', '=', 'out_invoice'),
                         ('state', '=', 'cancel')])
                    if len(invoice_ids.ids) == 0:
                        picking.create_credit_note_for_rma_in()
            elif picking.picking_type_code == 'outgoing' and picking.rma_id:
                if picking.state == 'done':
                    picking.create_invoice_for_rma_out()
        return validate_super

    def create_invoice_for_rma_out(self):
        sale_id = self.env['sale.order'].search([('name', '=', self.origin)])
        fiscal_position_id = self.env['account.fiscal.position']._get_fiscal_position(sale_id.partner_id)


        invoice_line_list = []
        for line in self.move_ids_without_package:
            taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == self.env.company)
            vals = (0, 0, {
                'name': line.product_id.display_name,
                'product_id': line.product_id.id,
                'price_unit': line.product_id.lst_price,
                'tax_ids': fiscal_position_id.map_tax(taxes),
                'quantity': line.quantity,
            })
            invoice_line_list.append(vals)

        current_user = self.env.uid

        move_record = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'invoice_origin': sale_id.name,
            'picking_id': self.id,
            'invoice_user_id': current_user,
            'narration': self.name,
            'partner_id': self.partner_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'rma_id': self.rma_id.id,
            'date': self.date or False,
            'fiscal_position_id': fiscal_position_id,
            'invoice_line_ids': invoice_line_list,
            'sale_id': self.rma_id.sale_order.id,
            'ref': self.rma_id.sale_order.client_order_ref,
            'team_id': sale_id.team_id.id
        })
        move_record.action_post()

    def create_credit_note_for_rma_in(self):
        sale_id = self.env['sale.order'].search([('name', '=', self.origin)])
        fiscal_position_id = self.env['account.fiscal.position'].with_context(
            {'rma_id': self.rma_id})._get_fiscal_position(self.partner_id)

        invoice_line_list = []
        for line in self.move_ids_without_package:
            sale_line_id = line.sale_line_id
            taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == self.env.company)
            vals = (0, 0, {
                'name': sale_line_id.product_id.display_name,
                'product_id': sale_line_id.product_id.id,
                'price_unit': sale_line_id.price_unit,
                'tax_ids': fiscal_position_id.map_tax(taxes),
                'quantity': line.quantity,
                # 'sale_line_ids': [(4, sale_line_id.id)],
                'discount': sale_line_id.discount if sale_line_id.discount else 0.0,
                'rma_line_id': line.rma_line_id.id,
                'stock_move_id': line.id,
            })
            invoice_line_list.append(vals)
        service_prds = self.rma_id.rma_line_ids.filtered(lambda
                                                             t: t.product_id.detailed_type == 'service' and t.price_unit > 0 and t.rma_reason_action == self.reason_action)
        if service_prds:
            for service_prd in service_prds.filtered(lambda service_prd: service_prd.delivery_qty > 0):
                vals = (0, 0, {
                    'name': service_prd.product_id.display_name,
                    'product_id': service_prd.product_id.id,
                    'price_unit': service_prd.price_unit,
                    'quantity': service_prd.delivery_qty,
                })
                invoice_line_list.append(vals)
        current_user = self.env.uid
        move_ids = self.env['account.move'].search(
            [('picking_id', '=', self.rma_id.delivery_order.id), ('move_type', '=', 'out_invoice'),
             ('state', '!=', 'cancel')], order='id DESC', limit=1)
        move_vals = {
            'move_type': 'out_refund',
            'invoice_origin': sale_id.name,
            'picking_id': self.id,
            'invoice_user_id': current_user,
            'narration': self.name,
            'partner_id': self.rma_id.inv_partner.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'rma_id': self.rma_id.id,
            'rma_id': self.rma_id.id,
            'ref': self.rma_id.sale_order.client_order_ref,
            'sale_id': self.rma_id.sale_order.id,
            'date': self.date or False,
            'fiscal_position_id': fiscal_position_id,
            'invoice_line_ids': invoice_line_list,
            'team_id': self.rma_id.sale_order.team_id.id,}
       
        move_record = self.env['account.move'].sudo().with_context(check_move_validity=False,
                                                                   skip_account_move_synchronization=True).create(
            move_vals)
        move_container = {'records': move_record}
        move_record._sync_dynamic_lines(move_container)
        move_record.action_post()

    def action_cancel(self):

        cancel_super = super(RmaStockPicking, self).action_cancel()

        cancel_picking_rma = self.env['rma.main'].search([('id', '=', self.rma_id.id)])

        cancel_picking_rma.update({
            'state': 'close',
        })

        return True

    
