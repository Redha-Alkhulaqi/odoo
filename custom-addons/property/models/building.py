from odoo import models, fields


class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
#   _rec_name = 'code'

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    name = fields.Char()
    active = fields.Boolean(default=True)