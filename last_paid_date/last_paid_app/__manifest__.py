# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Invoices Paid Amounts',
    'version': '14.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'author': "Odoo Tips",
    'website': 'https://www.facebook.com/OdooTips/',
    'depends': ['base', 'mail', 'account',
                ],
    'data': [
     'views/account_invoice_view.xml'
             ],
    'installable': True,
    'application': True,
}
