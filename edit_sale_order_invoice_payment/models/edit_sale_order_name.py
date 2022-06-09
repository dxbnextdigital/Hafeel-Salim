from odoo import models, fields, api

class EditSaleOrder(models.TransientModel):
        _name = 'edit.sale.order.name'
        name = fields.Char(string='Field Name')
        sale_order = fields.Many2one('sale.order')

        def action_update(self):
            self.sale_order.sudo().name = self.name

class EditSaleOrder(models.TransientModel):
        _name = 'edit.invoice.name'
        name = fields.Char(string='Field Name')
        invoice_id = fields.Many2one('account.move')

        def action_update(self):
            self.invoice_id.sudo().name = self.name




