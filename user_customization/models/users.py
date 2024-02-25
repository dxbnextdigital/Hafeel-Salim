from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
class ResUsers(models.Model):
    _inherit = 'res.users'

    custom_source_id = fields.Many2one(
        'custom.source.location',
        'Source'
    )

    journal_id = fields.Many2many('account.journal', domain=[('type', 'in', ('cash', 'bank'))])
    invoice_users_domain = fields.Char(string="Invoice Users id (',')")

