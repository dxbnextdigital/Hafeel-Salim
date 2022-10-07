

{
    'name': 'Total quantity in Sale Purchase Invoice',
    'version': '14.0.1.0.0',
    'summary': '',
    'description': '',
    'depends': ['purchase','sale','account'],
    'data': [
        'report/sale_order.xml',
        'report/purchase_order.xml',
        'report/account_move.xml'


    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
