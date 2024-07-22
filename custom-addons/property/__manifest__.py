{
    'name': "Property",
    'version': '1.0',
    'depends': ['base', 'mail'],
    'author': "Electron Technology",
    'category': 'Sales',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
    ],
    'assets': {
        'web.assets_backend': ['property/static/src/css/property.css']
    },
    'application': True,
}