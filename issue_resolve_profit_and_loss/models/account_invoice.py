# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import json
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = "account.move.line"
    cost_not_required = fields.Boolean(string="Avoid Cost")

    @api.onchange('cost_not_required')
    def check_status(self):
        print("uessss",self.cost_not_required)
        self.ensure_one()
        self._origin.cost_not_required = self.cost_not_required
