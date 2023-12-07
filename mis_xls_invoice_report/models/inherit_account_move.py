from odoo import api, fields, models, _


class InheritAccountMove(models.Model):
    _inherit='account.move.line'


    vat_amount=fields.Float(string='Vat amount',compute='_get_vat_amount')
    total_inc_vat=fields.Float(string='Total inc VAT',compute='_get_vat_amount')


    @api.depends('price_subtotal','tax_ids','quantity','price_unit')
    def _get_vat_amount(self):
        self.vat_amount=0
        self.total_inc_vat=0
        for rec in self:
            rec.vat_amount=sum(rec.price_subtotal * (taxes.amount/100) for taxes in rec.tax_ids)
            rec.total_inc_vat = rec.vat_amount + rec.price_subtotal



