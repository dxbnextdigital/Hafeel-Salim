from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_name_update_123(self):
        print("yes")
        return {'type': 'ir.actions.act_window',
                'name': 'Sale Order',
                'res_model': 'edit.sale.order.name',
                'target': 'new',
                'view_id': self.env.ref('edit_sale_order_invoice_payment.edit_sale_order_name_form_view').id,
                'view_mode': 'form',
                'context': {'default_sale_order': self.id}
                }


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_name_update_123(self):
        print("yes")
        print(self.id)
        return {'type': 'ir.actions.act_window',
                'name': 'Account Move',
                'res_model': 'edit.invoice.name',
                'target': 'new',
                'view_id': self.env.ref('edit_sale_order_invoice_payment.edit_invoice_name_form_view').id,
                'view_mode': 'form',
                'context': {'default_invoice_id': self.id}
                }

