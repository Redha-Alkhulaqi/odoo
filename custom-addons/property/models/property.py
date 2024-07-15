from odoo import models, fields, api

class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=True, default='New', size=100)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(0, 5))
    selling_price = fields.Float()
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


_sql_constraints = [
    ('unique_name', 'unique("name")', 'This name is exist!')
]

'''
@api.constrains('bedrooms')
def _check_bedrooms_greater_zero(self):
    for rec in self:
        if rec.bedrooms == 0:
            raise ValidationError('Please add valid number of bedrooms!')
'''

# CRUD OPERATION:

@api.model_create_multi
def create(self, vals):
    res = super(Property, self).create(vals)
    #  res = super().create(self, vals)
    print("inside create method")
    return res


@api.model
def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #  res = super()._search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None)
    print("inside search method")
    return res


def write(self, vals):
    res = super(Property, self).write(vals)
    #  res = super().write(self, vals)
    print("inside write method")
    return res


def unlink(self):
    res = super(Property, self).unlink()
    #  res = super().unlink(self)
    print("inside unlink method")
    return res