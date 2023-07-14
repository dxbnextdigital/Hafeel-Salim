from odoo import models, fields, api, _


class CustomSourceLocation(models.Model):
    _inherit = "custom.source.location"
    user_ids = fields.Many2many('res.users',string='Users')




class StockLocation(models.Model):
    _inherit = 'stock.location'
    user_ids = fields.Many2many('res.users',string='Users')

class ResCompany(models.Model):
    _inherit = "res.company"
    is_removed_restriction = fields.Boolean(string="Enable the restriction of sales person on location")

    @api.onchange('is_removed_restriction')
    def remove_access_sales_person_location(self):
        if self.is_removed_restriction:
            self.env.ref("user_specific_source_location.custom_source_user_location_rule").active = True
            self.env.ref("user_specific_source_location.restrict_custom_location_rule").active = True
        else:
            self.env.ref("user_specific_source_location.custom_source_user_location_rule").active = False
            self.env.ref("user_specific_source_location.restrict_custom_location_rule").active = False
