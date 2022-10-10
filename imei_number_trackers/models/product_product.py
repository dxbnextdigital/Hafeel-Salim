from odoo import fields, models, api,_

from odoo.exceptions import Warning, UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    is_imei_required = fields.Boolean(string="Is IMEI Required")

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_imei_visible = fields.Boolean(compute='check_imei_is_visible')

    imei_numbers_id = fields.One2many('imei.number','sale_order')

    def action_import_imei_numbers(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'imei.xls.import',
            'view_mode': 'form',
            'context': {'default_sale_order_id': self.id},
            'target': 'new'
        }

    def get_product(self, name):
        product = self.env['product.product'].search([('name', '=', name)], limit=1)
        if product:
            return product
        else:
            raise UserError(_('"%s" Product is not found in system !') % name)


    def pre_xls_entry_before(self,list):
        order_product = {}
        imei_product = {}
        if self.imei_numbers_id:
            for rec in self.order_line.filtered(lambda  p : p.product_id.product_tmpl_id.is_imei_required == True):
                order_product[rec.product_id.id] = rec.product_uom_qty
            for rec in self.imei_numbers_id:
                imei_product[rec.product_id.id] = 0
            for rec in self.imei_numbers_id:
                imei_product[rec.product_id.id] = imei_product[rec.product_id.id] + 1
            for rec in list:
                product_id = self.get_product(rec['Product'])
                if product_id:
                    imei_product[product_id.id] = imei_product[product_id.id]+1
            for rec in self.order_line:
            # print(order_product[rec.product_id.id])
            # print( imei_product)
                if  imei_product == {}:
                    raise UserError(_('Please enter IMEI Number'))

                else:
                    if order_product[rec.product_id.id] == imei_product[rec.product_id.id]:
                            pass
                    else:
                        raise UserError(_('Please check exceed limit  IMEI Number of Product '+rec.product_id.name))












    def check_imei_number_correct(self):
        is_ok = False
        order_product ={}
        imei_product ={}



        if self.imei_numbers_id:
            for rec in self.order_line.filtered(lambda  p : p.product_id.product_tmpl_id.is_imei_required == True):
                order_product[rec.product_id.id] = rec.product_uom_qty
            for rec in self.imei_numbers_id:
                imei_product[rec.product_id.id] = 0.0
            for rec in self.imei_numbers_id:
                imei_product[rec.product_id.id] = imei_product[rec.product_id.id]+1
            for rec in self.order_line:
                if  imei_product == {}:
                    raise UserError(_('Please enter IMEI Number'))

                else:
                    if order_product[rec.product_id.id] == imei_product[rec.product_id.id]:
                        return ;
                    else:
                        raise UserError(_('Please check IMEI Number of Product '+rec.product_id.name))
        else:
            raise UserError(_('Please enter IMEI Number'))

    def check_weather_is_imei_required(self):
        for rec in self.order_line:
            if rec.product_id.is_imei_required:
                self.is_imei_visible = True
                return True
        return False

    @api.depends('order_line')
    def check_imei_is_visible(self):
        self.is_imei_visible = False
        for rec in self.order_line:
            if rec.product_id.is_imei_required:
                self.is_imei_visible = True
                break




    def action_confirm_deliver(self):
        if self.check_weather_is_imei_required():
            self.check_imei_number_correct()
        return super(SaleOrder, self).action_confirm_deliver()


