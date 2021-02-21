from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
class ResUsers(models.Model):
    _inherit = 'res.users'

    custom_source_id = fields.Many2one(
        'custom.source.location',
        'Source'
    )

