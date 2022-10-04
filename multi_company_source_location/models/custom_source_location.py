from odoo import models, fields, api, _


class CustomSourceLocation(models.Model):
    _inherit = "custom.source.location"
    company_id = fields.Many2one('res.company',related='analytic_account_id.company_id')