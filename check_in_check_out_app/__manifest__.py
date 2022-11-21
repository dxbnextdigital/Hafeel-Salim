

{
    'name': 'Check In / Check Out',
    'version': '14.0.1.0.0',
    'summary': 'Check In / Check Out',
    'description': 'Check IN / Check Out',
    'depends': ['base'],
    'data': [
'security/ir.model.access.csv',
        'security/res_check.xml',
        'sequence/res_check.xml',
'views/res_check.xml',
'views/res_partner.xml'

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
