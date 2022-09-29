# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    quantity = fields.Float(
    'Quantity',
    help='Quantity of products in this quant, in the default unit of measure of the product',
    readonly=True,
        digits='Custom Report Inventory',
    )
    inventory_quantity = fields.Float(
        'Inventoried Quantity', compute='_compute_inventory_quantity',
        digits='Custom Report Inventory',
        inverse='_set_inventory_quantity', groups='stock.group_stock_manager')
    reserved_quantity = fields.Float(
        'Reserved Quantity',
        default=0.0,
        digits = 'Custom Report Inventory',
        help='Quantity of reserved products in this quant, in the default unit of measure of the product',
        readonly=True, required=True)
    available_quantity = fields.Float(
        'Available Quantity',
        digits='Custom Report Inventory',
        help="On hand quantity which hasn't been reserved on a transfer, in the default unit of measure of the product",
        compute='_compute_available_quantity')