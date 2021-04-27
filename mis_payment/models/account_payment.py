# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError, UserError

class account_payment(models.Model):
    _inherit = "account.payment"

    def do_print_payment(self):
         return self.env.ref('account.action_report_payment_receipt').report_action(self)

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Register Payment'

    def _filterjournal(self):

        if self.env.user.journal_id:
            listids=self.env.user.journal_id.ids
            return "[('company_id', '=', company_id),('type', 'in', ('bank', 'cash')), ('id', 'in', ("+ str(listids) +"))]"
        else:
            return "[('company_id', '=', company_id),('type', 'in', ('bank', 'cash'))]"

    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
                                 compute='_compute_journal_id',
                                 domain=_filterjournal)






