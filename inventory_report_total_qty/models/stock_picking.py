from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_qty = fields.Integer(compute = '_compute_total_line')
    total_qty_list = fields.Integer(compute = '_compute_total_line')

    @api.depends('move_ids_without_package')
    def _compute_total_line(self):
        count_list = 0
        count = 0
        if self.move_ids_without_package:
            for rec in  self.move_ids_without_package:
                count = count + rec.quantity_done
                count_list = count_list+rec.product_uom_qty

        self.total_qty = count
        self.total_qty_list = count_list
