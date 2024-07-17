from odoo import models, fields

class Taq(models.Model):
    _name = 'taq'

    name = fields.Char(required=True)
