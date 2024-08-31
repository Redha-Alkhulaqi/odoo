{
    'name': "Return Merchandise Authorization Management",
    "summary": "Return Merchandise Authorization (RMA)",
    'version': '1.0',
    'depends': ["stock_account"],
    'author': "Electron Technology",
    'category': 'RMA',
    'description': """
    Electron Technology's Return Merchandise Authorization (RMA) module provides companies with an easy, efficient means of tracking returned merchandise. It also includes flexible methods of dealing with the return or exchange of merchandise.
    """,

    'data': [
        "security/ir.model.access.csv",
        "views/menus.xml",
    ],
    "post_init_hook": "post_init_hook",
    'application': True,
}