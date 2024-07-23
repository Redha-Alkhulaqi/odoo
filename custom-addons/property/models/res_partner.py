from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    property_id = fields.Many2one('property')