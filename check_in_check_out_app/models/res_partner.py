from odoo import fields, models, api,_


class ResPartner(models.Model):
    _inherit ='res.partner'
    vist_count = fields.Integer('Digits', compute= '_compute_count_visit_partner')

    def action_visits(self):
        return {
            'name': _('Check In/Out'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,kanban',
            'res_model': 'res.check',
            'domain': [('partner_id','=',self.id)],
        }

    def _compute_count_visit_partner(self):
        self.vist_count =self.env['res.check'].search_count([('partner_id','=',self.id)])
