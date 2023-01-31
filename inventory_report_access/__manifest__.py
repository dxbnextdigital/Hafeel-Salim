# -*- coding: utf-8 -*-
{
    'name': "Custom Inventory Report",
    'version': '14.0.1.0',
    'license': 'Other proprietary',
    'category': 'Inventory Management',
    'summary': """Custom Inventory Report""",
    'description': """
Custom Inventory Report    """,
    'author': "Custom Inventory Report",
    'depends': [
        'stock',
        'stock_enterprise',
        'mis_xls_reports',
        'stock_account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_module_category.xml'
           ],
    'installable': True,
    'application': False,
}
