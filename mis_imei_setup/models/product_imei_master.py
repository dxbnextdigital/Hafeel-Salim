# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class ProductImei(models.Model):
    _name = 'product.imei'
    _description = 'Product IMEI'
    _rec_name = 'imei'

    imei = fields.Char(string='IMEI')
    partner_id = fields.Many2one('res.partner', string='Partner')
    invoice_id = fields.Many2one('account.move', string='Invoice No')
    invoice_date = fields.Date(string='Invoice Date')
    product_barcode = fields.Char(string='Product Barcode')
    product_id = fields.Many2one('product.product', string='Product')
    product_brand = fields.Many2one('product.category', string='Product Brand')
    so_line_id = fields.Many2one('sale.order.line', string='Sale Order Line')
    is_return = fields.Boolean(string='Return')
    so_id = fields.Many2one('sale.order', string='Sale Order')
    user_id = fields.Many2one('res.users', string='Sales Executive')
    team_id = fields.Many2one('crm.team', string='Sales Team')
    location_id = fields.Many2one('stock.location', string='Location')
    order_date = fields.Datetime(string='Order Date')

