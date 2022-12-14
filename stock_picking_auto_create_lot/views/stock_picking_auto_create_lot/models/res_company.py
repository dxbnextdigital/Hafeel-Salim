from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    lot_sequence = fields.Char(string="Lot Sequence")
