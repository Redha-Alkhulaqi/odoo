from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):
    
    def setup(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref': 'PRT10000',
            'name': 'Property 10000',
            'description': 'Property 10000 description',
            'postcode': '10101',
            'date_availability': fields.Date.today(),
            'expected_selling_date': fields.Date.today(),
            'is_late': True,
            'expected_price': 10000,
            'selling_price': 10000,
            'diff': 0,
            'bedrooms': 10,
            'living_area': 10,
            'facades': 10,
            'garage': True,
            'garden': True,
            'garden_area': 200,
            'garden_orientation': 'north',
            'state': 'draft',
        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id, [{
            'ref': 'PRT10000',
            'name': 'Property 10000',
            'description': 'Property 10000 description',
            'postcode': '10101',
            'date_availability': fields.Date.today(),
            'expected_selling_date': fields.Date.today(),
            'is_late': True,
            'expected_price': 10000,
            'selling_price': 10000,
            'diff': 0,
            'bedrooms': 10,
            'living_area': 10,
            'facades': 10,
            'garage': True,
            'garden': True,
            'garden_area': 200,
            'garden_orientation': 'north',
            'state': 'draft',
        }])
    
