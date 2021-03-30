from odoo import models, fields

class MisStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    partner_id = fields.Many2one('res.partner', related='move_id.partner_id', stored=True)
    price_unit = fields.Float(compute='_compute_price_unit', stored=True)
    cost_price = fields.Float(related='product_id.standard_price', stored=True)

    def _compute_price_unit(self):
        for rec in self:
            if rec.move_id.purchase_line_id:
                rec.price_unit = rec.move_id.purchase_line_id.price_unit
            elif rec.move_id.sale_line_id:
                rec.price_unit = rec.move_id.sale_line_id.price_unit
            elif rec.move_id.price_unit:
                rec.price_unit = rec.move_id.price_unit
            else:
                rec.price_unit = rec.product_id.list_price

