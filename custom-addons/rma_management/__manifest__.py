{
    'name': "Return Merchandise Authorization Management",
    "summary": "Return Merchandise Authorization (RMA)",
    'version': '1.0',
    'depends': ['base'],
    'author': "Electron Technology",
    'category': 'Sales',
    'description': """
    Electron Technology's Return Merchandise Authorization (RMA) module provides companies with an easy, efficient means of tracking returned merchandise. It also includes flexible methods of dealing with the return or exchange of merchandise.
    """,

    'data': [
        "security/ir.model.access.csv",
        "wizard/stock_picking_return_views.xml",
        "wizard/rma_delivery_views.xml",
        "wizard/rma_finalization_wizard_views.xml",
        "wizard/rma_split_views.xml",
        "views/menus.xml",
        "views/res_partner_views.xml",
        "views/rma_finalization_views.xml",
        "views/rma_portal_templates.xml",
        "views/rma_team_views.xml",
        "views/rma_views.xml",
        "views/rma_tag_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_warehouse_views.xml",
        "views/res_config_settings_views.xml",
    ],
    'application': True,
}