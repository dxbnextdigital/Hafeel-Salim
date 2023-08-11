# See LICENSE file for full copyright and licensing details.
from odoo import fields, models
from datetime import datetime, date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    block_nonpayment = fields.Boolean('Block for Non Payment?', default=False)
    print_name = fields.Char(string='Print Name')


    def check_overdue_invoice_cron_job(self):
        partner_ids = self.env['res.partner'].search([])
        partner_ids.write({"over_credit": False, "block_nonpayment": False})
        invoice_ids = self.env['account.move'].search([]).filtered(lambda o:(o.payment_state in ['not_paid', 'partial']) and (o.state == 'posted') and (o.journal_id.type == 'sale'))
        today = datetime.today().date()
        for invoice_id in invoice_ids:
            remaining_days = today - invoice_id.invoice_date_due
            if remaining_days.days > 15:
                invoice_id.partner_id.block_nonpayment = True
    
