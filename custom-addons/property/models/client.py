from odoo import models


class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'