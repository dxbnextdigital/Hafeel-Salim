# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import json
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = "account.move"
    last_paid_date = fields.Date(compute='_compute_last_paid' ,string='Paid Date',store=True)
    paid_amount = fields.Float(compute ='_compute_paid_amount',string="Payment Amount")

    @api.depends('amount_total_signed','amount_residual')
    def _compute_paid_amount(self):
        for rec in self:
            rec.paid_amount = rec.amount_total_signed - rec.amount_residual


    def _compute_last_paid(self):
        for rec in self:
            payments = json.loads(rec.invoice_payments_widget)
            if payments:
                date =[]
                for  dates in payments['content']:

                    date.append(datetime.strptime(dates['date'], '%Y-%m-%d'))
                date = sorted(date)


                rec.last_paid_date = date[-1]
            else:
                rec.last_paid_date = False
