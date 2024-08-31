from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    rma_team_id = fields.Many2one(
        comodel_name="rma.team",
        string="RMA Team",
        help="RMA Team the user is member of.",
    )