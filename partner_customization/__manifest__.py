{
    'name': 'Partner Customization',
    'version': '13.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'author': 'Mindinfosys FZE LLC',
    'website': 'http://www.mindinfosys.com/',
    'maintainer': 'Mindinfosys FZE LLC',
    'summary': 'Add print name and Block non payment',
    'depends': ['base','base_setup','sale_management',
        ],
    'data': [
        'views/partner_view.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'auto_install': False,
}
