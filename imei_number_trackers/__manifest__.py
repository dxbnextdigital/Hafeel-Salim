

{
    'name': 'IMEI TRACKER',
    'version': '14.0.1.0.0',
    'summary': '',
    'description': '',
    'depends': ['account','sale','sale_management','stock','sales_source_location'],
    'data': [
        'security/ir.model.access.csv',
        'security/recording_rule.xml',
        'views/assets.xml',
'views/sale_order.xml',
        'views/imei_number.xml',
        'views/product_template.xml',
        'views/stock_picking.xml',
        'views/imei_Return/imei_return.xml',
        'wizard/imei_xlsx_import.xml',
        'wizard/imei_xlsx_import_return.xml'


    ],
    'qweb': ['static/xml/imei_scaning_screen_sale.xml',
             'static/xml/imei_scaning_screen_return.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
