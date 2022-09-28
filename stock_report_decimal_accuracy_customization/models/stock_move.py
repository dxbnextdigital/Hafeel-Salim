
from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):
    _inherit = 'stock.move'
    product_qty = fields.Float(
        'Real Quantity', compute='_compute_product_qty', inverse='_set_product_qty',
        store=True, compute_sudo=True,
        digits='Custom Report Inventory',
        help='Quantity in the default UoM of the product')
    availability = fields.Float(
        'Forecasted Quantity', compute='_compute_product_availability',        digits='Custom Report Inventory',
        readonly=True, help='Quantity in stock that can still be reserved for this move')

    product_qty_onhand = fields.Float(
        string='Onhand Quantity',
        digits='Custom Report Inventory'

    )
