from odoo import models, fields,api
import json
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    journal_domain = fields.Char(compute='_compute_journal_user')



    @api.depends('user_id','journal_id')
    def _compute_journal_user(self):

        current_uid = self.env.user.journal_id.mapped("id")
        self.journal_domain = str([('id', '=', current_uid)])
        if self.env.user.journal_id:
            self.journal_domain= json.dumps([('id', '=', current_uid),('type', 'in', ('bank', 'cash'))])
        else:
            self.journal_domain=  json.dumps([('type', 'in', ('bank', 'cash'))])


