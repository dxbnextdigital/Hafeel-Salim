from odoo import models, fields

class MisStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    partner_id = fields.Many2one('res.partner', related='move_id.partner_id', stored=True)
    price_unit = fields.Float(related='move_id.price_unit', stored=True)
    cost_price = fields.Float(related='product_id.standard_price', stored=True)

