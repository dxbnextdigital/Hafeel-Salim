
from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):
    _inherit = 'report.stock.quantity'
    product_qty = fields.Float(string='Quantity',        digits='Custom Report Inventory', readonly=True)

class StockValuationLayer(models.Model):
    _inherit ='stock.valuation.layer'
    quantity = fields.Float('Quantity', digits='Custom Report Inventory', help='Quantity', readonly=True)
    remaining_qty = fields.Float(digits='Custom Report Inventory', readonly=True)
