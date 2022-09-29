from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_qty = fields.Integer(compute = '_compute_total_line')

    @api.depends('move_ids_without_package')
    def _compute_total_line(self):
        count = 0
        if self.move_ids_without_package:
            for rec in  self.move_ids_without_package:
                count = count + rec.quantity_done

        self.total_qty = count
