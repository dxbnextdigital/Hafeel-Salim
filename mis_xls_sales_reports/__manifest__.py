{
    'name': 'MiS XLS Sales Reports',
    'version': '13.0.1',
    'summary': "XLS Sales Reports",
    'description': "XLS Reports for Sales",
    'category': 'Warehouse',
    'author': 'mindinfosys.com',
    'maintainer': 'mindinfosys.com',
    'company': 'mindinfosys.com',
    'website': 'http://www.mindinfosys.com',
    'depends': [
                'base',
                'stock',
                'sale',
                'purchase',
                ],
    'data': [
            'views/wizard_view.xml',
            'views/action_manager.xml',
            'security/ir.model.access.csv',
            ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'auto_install': False,
}
