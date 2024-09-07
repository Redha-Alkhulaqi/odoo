# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    b2b_source_picking_type_id = fields.Many2one('stock.picking.type', string="Source Picking Type ",
                                                 related='company_id.b2b_source_picking_type_id', readonly=False)
    b2b_without_return_items_picking_type_id = fields.Many2one('stock.picking.type',
                                                               string="Without return items picking type",
                                                               related='company_id.b2b_without_return_items_picking_type_id',
                                                               readonly=False)
    b2b_rma_out_route_id = fields.Many2one('stock.route', string="RMA Route for SO",
                                           related='company_id.b2b_rma_out_route_id', readonly=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        b2b_source_picking_type_id = ICPSudo.get_param('bi_rma.b2b_source_picking_type_id')
        b2b_without_return_items_picking_type_id = ICPSudo.get_param('bi_rma.b2b_without_return_items_picking_type_id')
        b2b_rma_out_route_id = ICPSudo.get_param('bi_rma.b2b_rma_out_route_id')

        vals = {}
        if b2b_source_picking_type_id:
            vals['b2b_source_picking_type_id'] = int(b2b_source_picking_type_id)
        if b2b_without_return_items_picking_type_id:
            vals['b2b_without_return_items_picking_type_id'] = int(b2b_without_return_items_picking_type_id)
        if b2b_rma_out_route_id:
            vals['b2b_rma_out_route_id'] = int(b2b_rma_out_route_id)
        if vals:
            res.update(vals)

        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        ICPSudo.set_param('bi_rma.b2b_source_picking_type_id', self.b2b_source_picking_type_id.id)
        ICPSudo.set_param('bi_rma.b2b_rma_out_route_id', self.b2b_rma_out_route_id.id)
        ICPSudo.set_param('bi_rma.b2b_without_return_items_picking_type_id',
                          self.b2b_without_return_items_picking_type_id.id)


class ResCompany(models.Model):
    _inherit = 'res.company'

    b2b_source_picking_type_id = fields.Many2one('stock.picking.type')
    b2b_without_return_items_picking_type_id = fields.Many2one('stock.picking.type')
    b2b_rma_out_route_id = fields.Many2one('stock.route')
