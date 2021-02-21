{
    'name': 'Product Customization',
    "version": "14.0.1.0.0",
    'author': 'mindinfosys',
    'website': 'http://www.mindinfosys.com/',
    'license': 'LGPL-3',
    'installable': True,
    'summary': 'Adding additional field in product master',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
}
