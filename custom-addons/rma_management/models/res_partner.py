from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    test1 = fields.Char()
    test2 = fields.Char()
    test3 = fields.Char()
    rma_ids = fields.One2many(
        comodel_name="rma",
        inverse_name="partner_id",
        string="RMAs",
    )
    rma_count = fields.Integer(
        string="RMA count",
        compute="_compute_rma_count",
    )
