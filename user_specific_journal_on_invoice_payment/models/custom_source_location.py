from odoo import models, fields, api, _
import json
class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    journal_id_domain = fields.Char(compute="_compute_domain_payment_register",
    readonly=True,
    store=False,)


    @api.depends('journal_id')
    def _compute_domain_payment_register(self):

        if self.env.user.journal_id:
            for journal in  self.env.user.journal_id.id:
                self.journal_id = journal
                break
            self.journal_id_domain = json.dumps([('id', 'in', self.env.user.journal_id.mapped('id'))])
        else:
            self.journal_id_domain = json.dumps([('type', 'in', ('cash', 'bank'))])

