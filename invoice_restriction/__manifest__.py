

{
    'name': 'Invoice Restriction',
    'version': '14.0.1.0.0',
    'summary': '',
    'description': '',
    'depends': ['account'],
    'data': [
        'security/invoice_invisible_group.xml',
        'views/restricted_user_invoice.xml'

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
