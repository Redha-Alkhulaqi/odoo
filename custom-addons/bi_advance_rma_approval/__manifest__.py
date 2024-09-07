# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
	"name":"Advance RMA - Return Orders Management | Return Merchandise Authorization",
	"version":"17.0.0.1",
	"category":"Sales",
	"summary":"Create RMA Return Orders Request Approval for Sales Return Merchandise Authorization Rejection RMA Customer Product Replacement RMA Product Return Request RMA Product Refund Order Approve RMA Product Request Reject Sale RMA Return Order Management Approval",
	"description":"""
        
        Return Merchandise Authorization Odoo apps is used to allow your customer to manage return of the products and create return RMA order in Backend with complete process. i.e Return product from RMA, Replace Product with RMA, Refund Order from RMA, Refund invoice with RMA and everything managed with different stage.
	
    """,
    "author": "BrowseInfo",
    "price": 100,
    "currency": "EUR",
    "website" : "https://www.browseinfo.com",
    "depends":["base",
               "bi_rma",
              ],
	"data":[
            "security/bi_advance_rma_approval_security.xml",
            "security/ir.model.access.csv",
            "views/rma_view.xml",
           ],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/Oxqs2odfNv0',
    "images":['static/description/Return-Merchandise-Authorization-Banner.gif'],
}
