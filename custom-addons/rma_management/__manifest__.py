{
    'name': "Return Merchandise Authorization Management",
    "summary": "Return Merchandise Authorization (RMA)",
    'version': '1.0',
    'depends': ['base', 'sale_management', 'account_accountant', 'mail', "stock_account"],
    'author': "Electron Technology",
    'category': 'Sales',
    'description': """
    Electron Technology's Return Merchandise Authorization (RMA) module provides companies with an easy, efficient means of tracking returned merchandise. It also includes flexible methods of dealing with the return or exchange of merchandise.
    """,

    'data': [
        "security/ir.model.access.csv",
        "views/menus.xml",
    ],
    'application': True,
}