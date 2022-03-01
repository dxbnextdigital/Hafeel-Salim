from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_imei_required = fields.Boolean(string='Is IMEI Required', default=False)

    
    