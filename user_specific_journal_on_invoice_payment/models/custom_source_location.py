from odoo import models, fields, api, _
import json
class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    journal_id_domain = fields.Char(compute="_compute_domain_payment_register",
    readonly=True)

    @api.depends('can_edit_wizard', 'company_id')
    def _compute_journal_id(self):
        super()._compute_journal_id()
        if self.env.user.journal_id:
            self.journal_id = False



    @api.depends('journal_id')
    def _compute_domain_payment_register(self):


        if self.env.user.journal_id:

            self.journal_id_domain = json.dumps([('id', 'in', self.env.user.journal_id.mapped('id'))])
        else:
            self.journal_id_domain = json.dumps([('type', 'in', ('cash', 'bank'))])



