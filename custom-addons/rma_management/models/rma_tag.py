from odoo import fields, models


class RmaTag(models.Model):
    _description = "RMA Tags"
    _name = "rma.tag"
    _order = "name"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the category without removing it.",
    )
    name = fields.Char(string="Tag Name", required=True)
    is_public = fields.Boolean(string="Public Tag", help="The tag is visible in the portal view")
    color = fields.Integer(string="Color Index")
    rma_ids = fields.Many2many('rma')

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists !"),
    ]