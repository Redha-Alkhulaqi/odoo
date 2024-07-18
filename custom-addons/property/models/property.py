from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=True, default='New', size=15)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(0, 2))
    selling_price = fields.Float(digits=(0, 2))
    diff = fields.Float(compute='_compute_diff', store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='draft')

    _sql_constraints = [
    ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            return {
                'warning': {'title': 'warning', 'message': 'negative value', 'type': 'notification'}
            }
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms!')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'