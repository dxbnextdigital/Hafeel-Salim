from odoo import models, fields, _, exceptions
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_report_data(self):
        record_collection = []
        for each in self.invoice_line_ids:
            so_id = self.env['sale.order'].search([('name', '=', self.payment_reference)])
            record_collection = self.env['product.imei'].search([('product_id', '=', each.product_id.id),
                                                                 ('so_id','=',so_id.id)]).filtered(lambda o:(o.product_id.product_tmpl_id.is_imei_required == True)).mapped('imei')
        print('record_collection>>>>>>>>', record_collection)
        return record_collection