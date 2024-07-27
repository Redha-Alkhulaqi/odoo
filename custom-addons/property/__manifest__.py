{
    'name': "Property",
    'version': '1.0',
    'depends': ['base', 'sale_management', 'account_accountant', 'mail'],
    'author': "Electron Technology",
    'category': 'Sales',
    'description': """
    Description text
    """,

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': ['property/static/src/css/property.css']
    },
    'application': True,
}