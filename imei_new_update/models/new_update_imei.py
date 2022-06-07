from odoo import fields, models, api,_
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError

class test(models.Model):
    _name= 'test.imei.one'
    _rec_name ="product_id"
    product_id = fields.Many2one('product.product')
    imei_update_new_id = fields.Many2one('imei.update.new')
    imei_number = fields.Char()
    status = fields.Selection([('return', 'return'), ('used', 'used')])


    @api.constrains('imei_number')
    def _check_date_end(self):
        for rec in self:
            check_exist = self.env['test.imei.one'].search([('status','=','used'),('product_id','=',rec.product_id.id),('imei_number','=',rec.imei_number)])
            print(check_exist)
            if check_exist:
                raise ValidationError("This imei number already used for this product")


class ImeiUpdateNew(models.Model):
    _name = 'imei.update.new'
    domain_fixed = fields.Boolean(compute="domain_fix")
    sale_order_id = fields.Many2one('sale.order')
    sale_order_lines = fields.Many2one('sale.order.line')
    numbers_emi = fields.Float(related='sale_order_lines.product_uom_qty')
    new_product_imei = fields.One2many('test.imei.one','imei_update_new_id')
    order_id = fields.Integer(related='sale_order_id.id')


    @api.onchange('sale_order_lines')
    def onchange_method(self):
        lines =[]
        for rec in range(0,int(self.numbers_emi)):
            vals= {
                'product_id': self.sale_order_lines.product_id.id,
                'status' : 'used'
            }
            lines.append((0,0,vals))

        self.new_product_imei =lines
        temp = [i.product_id.id for i in self.new_product_imei]
        return {"domain" :{'sale_order_lines':[('product_id.id','not in',temp),('order_id','=',self.sale_order_id.id)]}}



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    imei_update_new_id = fields.Many2one('imei.update.new')
    def capture_imei(self):
        if self.imei_update_new_id:
            pass
        else:
            self.imei_update_new_id=self.imei_update_new_id.create({
                'sale_order_id' : self.id
            })

        view = self.env.ref('imei_new_update.imei_new_update_form_view')
        return {
                'name': _('Scan IMEI Numbers'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'imei.update.new',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': self.imei_update_new_id.id,
                 'context': {'default_sale_order_id' : self.id}
         }


