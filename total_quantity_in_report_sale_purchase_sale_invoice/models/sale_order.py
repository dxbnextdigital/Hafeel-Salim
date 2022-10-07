from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_qty = fields.Integer(compute='_compute_total_quantity')

    @api.depends('order_line')
    def _compute_total_quantity(self):
        total_qty =0
        for rec in self.order_line:
            total_qty = total_qty+ rec.product_uom_qty
        self.total_qty = total_qty
class PurchaseOrder(models.Model):
    _inherit ='purchase.order'

    total_qty = fields.Integer(compute='_compute_total_quantity')

    @api.depends('order_line')
    def _compute_total_quantity(self):
        total_qty =0
        for rec in self.order_line:
            total_qty = total_qty+ rec.product_uom_qty
        self.total_qty = total_qty


class SaleOrder(models.Model):
    _inherit = 'account.move'

    total_qty = fields.Integer(compute='_compute_total_quantity')

    def _compute_total_quantity(self):
        total_qty =0
        for rec in self.invoice_line_ids:
            total_qty = total_qty + rec.quantity
        self.total_qty = total_qty