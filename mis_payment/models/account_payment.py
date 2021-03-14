# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError, UserError

class account_payment(models.Model):
    _inherit = "account.payment"

    def do_print_payment(self):
         return self.env.ref('account.action_report_payment_receipt').report_action(self)


