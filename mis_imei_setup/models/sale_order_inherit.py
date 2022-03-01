from odoo import models, fields, _, exceptions
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm_deliver(self):
        for each in self.order_line:
            if each.product_id.product_tmpl_id.is_imei_required == True:
                so_line_imei_ids = self.env['product.imei'].search([('is_return', '=', False),('so_id', '=', each.order_id.id)])
                product_imeis = self.env['product.imei'].search([('is_return', '=', False)]).mapped('imei')
                duplicates=[]
                for product_imei in product_imeis:
                    for record in so_line_imei_ids.mapped('imei'):
                        if product_imei == record:
                            duplicates.append(product_imei)
                if len(duplicates) != len(set(duplicates)):
                    raise exceptions.ValidationError(_("Duplicate IMEI found for product %(product_name)s in line %(orderline)s") 
                        % {'product_name': each.name, 'orderline': len(each)})
                elif each.total_imei > each.product_uom_qty:
                    raise exceptions.ValidationError(_("Scanned IMEI is more than the required quantity for product %(product_name)s in line %(orderline)s") 
                        % {'product_name': each.name, 'orderline': len(each)})
                elif each.total_imei < each.product_uom_qty:
                    raise exceptions.ValidationError(_("Scanned IMEI is less than the required quantity for product %(product_name)s in line %(orderline)s") 
                        % {'product_name': each.name, 'orderline': len(each)})
        res = super(SaleOrder, self).action_confirm_deliver()
        so_line_imei_ids.write({'invoice_id': self.invoice_ids[0].id,
                                'invoice_date': self.invoice_ids[0].invoice_date
                                })


    def get_data(self):
        record_collection = []
        for each in self.order_line:
            if each.product_id.product_tmpl_id.is_imei_required == True:
                product_imeis = self.env['product.imei'].search([('product_id', '=', each.product_id.id),
                                                                ('so_line_id','=',each.id)]).mapped('imei')
            record_collection = self.env['product.imei'].search([('product_id', '=', each.product_id.id),
                                                                ('so_line_id','=',each.id)]).filtered(lambda o:(o.product_id.product_tmpl_id.is_imei_required == True)).mapped('imei')
        return record_collection

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    total_imei = fields.Integer(string='Total IMEI', store=True, copy=False)


    def capture_imei(self):            
        view = self.env.ref('mis_imei_setup.imei_capture_wiz_view')
        if self.product_id.product_tmpl_id.is_imei_required == True:
            product_imei_ids = self.env['product.imei'].search([('product_id', '=', self.product_id.id),
                                                                ('so_line_id','=',self.id)])
            print('kdhssodo', product_imei_ids.mapped('imei'))
            wiz = self.env['imei.capture.wiz'].create({'product_id': self.product_id.id,
                                                       'partner_id': self.order_id.partner_id.id,
                                                       'product_quantity' : self.product_uom_qty,
                                                       'imei_line_ids': [(0, 0, {'imei': product_imei_id.imei})
                                                                         for product_imei_id in product_imei_ids]})
            return {
                'name': _('Scan IMEI Numbers'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'imei.capture.wiz',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }
        else:
            raise ValidationError("IMEI is disabled for the product.")

