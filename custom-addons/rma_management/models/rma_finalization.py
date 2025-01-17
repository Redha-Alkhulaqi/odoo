from odoo import fields, models


class RmaFinalization(models.Model):
    _description = "RMA Finalization Reason"
    _name = "rma.finalization"
    _order = "name"

    active = fields.Boolean(default=True)
    name = fields.Char(
        string="Reason Name",
        required=True,
        translate=True,
        copy=False,
    )
    company_id = fields.Many2one('res.company')

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique (name, company_id)",
            "Finalization name already exists !",
        ),
    ]