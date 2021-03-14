# -*- coding: utf-8 -*-
{
    'name': 'MIS Payment Customization',
    'version': '13.0.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Payment Customization',
    'description': """
This module allows to print your payments.

    """,
    'website': 'http://www.mindinfosys.com',
    'depends' : ['payment', 'account'],
    'data': [
        'views/account_payment.xml',
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
