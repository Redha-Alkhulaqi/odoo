{
    'name': "Property",
    'version': '17.0.0.1.0',
    'depends': ['base'],
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
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
    'application':True,
}