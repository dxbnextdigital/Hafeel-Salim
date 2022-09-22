{
    'name': 'XLS Invoice Reports Sales Team',
    'version': '13.0.1',
    'summary': "XLS Invoice Reports",
    'description': "XLS Reports for Invoice",
    'category': 'Accounting',
    'depends': [
                'base',
                'stock',
                'sale',
                'purchase',
                'account','mis_xls_invoice_report'
                ],
    'data': [
            # 'views/wizard_view.xml',
        'security/ir.model.access.csv',
'security/group_to_hide_margin.xml',
        'views/action_manager.xml',
            'views/invoice_product_wizard_view.xml'
            # 'views/crditnote_wizard_view.xml',
            ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'auto_install': False,
}
