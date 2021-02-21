from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Many2one('mis.product.brand', string='Brand')
    color = fields.Many2one('mis.product.color', string='Color')
    min_sale_price = fields.Float(string='Min. Sales Price', default=0.00)
    generation = fields.Char(string='Connectivity')
    screen_size = fields.Char(string='Screen Size')
    model_no = fields.Char(string='Model No')

class MisColProductBrand(models.Model):
    _name = 'mis.product.brand'
    _description = 'Product Band'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Brand",  required=True, track_visibility='onchange')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Product Brand !"),
    ]

class MisProductColor(models.Model):
    _name = 'mis.product.color'
    _description = 'Product Color'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Color",  required=True, track_visibility='onchange')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Product Color !"),
    ]