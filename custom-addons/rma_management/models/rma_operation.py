from odoo import fields, models


class RmaOperation(models.Model):
    _name = "rma.operation"
    _description = "RMA requested operation"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, translate=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "That operation name already exists !"),
    ]