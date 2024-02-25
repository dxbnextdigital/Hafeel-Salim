from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

from odoo import models, fields





class ResUsers(models.Model):
    _inherit = 'res.users'

    custom_source_id = fields.Many2one(
        'custom.source.location',
        'Source'
    )
    source_users_invoice_restriction = fields.Char(string="Invoice User Ids With (-)")
    journal_id = fields.Many2many('account.journal', domain=[('type', 'in', ('cash', 'bank'))])

