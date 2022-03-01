# -*- coding: utf-8 -*-
{
    'name': 'MIS IMEI Numbers Tracking',
    'version': '13.0.0.0',
    'category': 'Sales',
    'summary': 'IMEI Numbers Tracking',
    'description': """
This module allows to track IMEI from sales orders.

    """,
    'website': 'http://www.mindinfosys.com',
    'depends' : ['base', 'account', 'sale', 'stock', 'sales_source_location', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_inherit.xml',
        'views/sale_order_inherit.xml',
        'views/product_imei_master_view.xml',
        'views/stock_picking_inherit.xml',
        'wizard/imei_capture_wiz_view.xml',
        'wizard/imei_return_wiz_view.xml',
        'reports/quotation_report_inherit.xml',
        'reports/invoice_report_inherit.xml',

    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
