# -*- coding: utf-8 -*-
{
    'name': "Sales Source Location",
    'version': '14.0.1.0',
    'license': 'Other proprietary',
    'category': 'Invoicing Management',
    'summary': """Sales Stock location""",
    'description': """
        Sales Stock location.
    """,
    'author': "Mindinfsys",
    'website': 'www.mindinfosys.com',
    'depends': ['base','sale','stock', 'base_setup',],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/source_location_view.xml',
        'views/stock_view.xml',
    ],
    'installable': True,
    'application': False,
}
