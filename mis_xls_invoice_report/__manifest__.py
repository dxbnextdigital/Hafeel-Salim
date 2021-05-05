{
    'name': 'MiS XLS Invoice Reports',
    'version': '13.0.1',
    'summary': "XLS Invoice Reports",
    'description': "XLS Reports for Invoice",
    'category': 'Accounting',
    'author': 'mindinfosys.com',
    'maintainer': 'mindinfosys.com',
    'company': 'mindinfosys.com',
    'website': 'http://www.mindinfosys.com',
    'depends': [
                'base',
                'stock',
                'sale',
                'purchase',
                'account'
                ],
    'data': [
            'views/wizard_view.xml',
            'views/action_manager.xml',
            'views/crditnote_wizard_view.xml',
            'security/ir.model.access.csv',
            ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'auto_install': False,
}
