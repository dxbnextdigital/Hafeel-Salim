from odoo import models, fields, _, exceptions,api
from odoo.exceptions import ValidationError

# class AccountMove(models.Model):
#     _inherit = 'crm.team'
#
#     def write(self, vals):
#         print('vals',vals)
#         for rec in self.member_ids:
#
#             print(rec.name)
#
#         return super(AccountMove, self).write(vals)