# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models, exceptions
from odoo.exceptions import ValidationError

class Picking(models.Model):
    _inherit = 'stock.picking'


    def button_validate(self):
        if self.picking_type_id.code == 'incoming':
            for each in self.move_ids_without_package:
                if each.product_id.product_tmpl_id.is_imei_required == True:
                    if each.total_ret_imei > each.product_uom_qty:
                        raise exceptions.ValidationError(_("Scanned IMEI is more than the required quantity for product %(product_name)s in line %(orderline)s") 
                            % {'product_name': each.name, 'orderline': len(each)})
                    if each.total_ret_imei < each.product_uom_qty:
                        raise exceptions.ValidationError(_("Scanned IMEI is less than the required quantity for product %(product_name)s in line %(orderline)s") 
                            % {'product_name': each.name, 'orderline': len(each)})

        res = super(Picking, self).button_validate()
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    total_ret_imei = fields.Integer(string='Total IMEI', store=True, copy=False)


    def capture_return_imei(self):
        view = self.env.ref('mis_imei_setup.imei_return_wiz_view')
        if self.product_id.product_tmpl_id.is_imei_required == True:
            product_imei_ids = self.env['product.imei'].search([('product_id', '=', self.product_id.id),
                                                                ('so_line_id','=',self.sale_line_id.id)])
            wiz = self.env['imei.return.wiz'].create({'product_id': self.product_id.id,
                                                      'partner_id': self.partner_id.id,
                                                      'ret_product_quantity' : self.product_uom_qty,
                                                      'ret_imei_line_ids': [(0, 0, {'imei': product_imei_id.imei,
                                                                                     'is_return':product_imei_id.is_return})
                                                                         for product_imei_id in product_imei_ids]
                                                                         })
            return {
                'name': _('Return IMEI Number'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'imei.return.wiz',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': {'current_id': self.id},
            }
        else:
            raise ValidationError("IMEI is disabled for the product.")
