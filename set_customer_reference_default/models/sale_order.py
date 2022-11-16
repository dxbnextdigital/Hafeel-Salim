from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    customer_reference = fields.Char(string='Customer Reference',related='partner_id.ref')
    client_order_ref = fields.Char(string='Reference')
