from odoo import fields, models, api, _
# from datetime import date, time, datetime
# from odoo.exceptions import UserError, Warning, ValidationError, AccessError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    rma_id = fields.Many2one('rma.main', 'RMA Id')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    return_order_line_id = fields.One2many('rma.lines', 'sale_line_id')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    rma_line_id = fields.Many2one('rma.lines')
    stock_move_id = fields.Many2one('stock.move')

class AccountMove(models.Model):
    _inherit = 'account.move'

    rma_id = fields.Many2one('rma.lines', 'RMA Id.')
    picking_id = fields.Many2one('stock.picking','Picking')
    sale_id  =  fields.Many2one('sale.order', 'Sale Origin')
    rma_id = fields.Many2one('rma.main', 'RMA Id')
