# See LICENSE file for full copyright and licensing details.
from odoo import fields, models
class ResPartner(models.Model):
    _inherit = 'res.partner'

    over_credit = fields.Boolean('Allow Over Credit?', default=True)
    block_nonpayment = fields.Boolean('Block for Non Payment?', default=False)
    print_name = fields.Char(string='Print Name', required=True)
