from odoo import fields, models, api,_

from odoo.exceptions import Warning, UserError, ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_imei_visible = fields.Boolean(compute='check_imei_is_visible')

    imei_numbers_id = fields.One2many('imei.number.return','picking_id')

    def action_import_imei_numbers(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'xlsx.imei.return',
            'view_mode': 'form',
            'context': {'default_picking_id': self.id},
            'target': 'new'
        }

    @api.depends('move_ids_without_package')
    def check_imei_is_visible(self):
        self.is_imei_visible = False
        if self.check_is_it_return():

            for rec in self.move_ids_without_package:
                if rec.product_id.is_imei_required:
                    self.is_imei_visible = True
                    break



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
            for rec in self.move_ids_without_package.filtered(lambda  p : p.product_id.product_tmpl_id.is_imei_required == True):
                order_product[rec.product_id.id] = rec.product_uom_qty
            for rec in self.imei_numbers_id:
                imei_product[rec.product_id.id] = 0
            for rec in self.imei_numbers_id:
                imei_product[rec.product_id.id] = imei_product[rec.product_id.id] + 1
            for rec in list:
                product_id = self.get_product(rec['Product'])
                if product_id:
                    imei_product[product_id.id] = imei_product[product_id.id]+1
            for rec in self.move_ids_without_package:
            # print(order_product[rec.product_id.id])
            # print( imei_product)
                if  imei_product == {}:
                    raise UserError(_('Please enter IMEI Number'))

                else:
                    if order_product == imei_product:
                            return ;
                    else:
                        raise UserError(_('Please check exceed limit  IMEI Number of Product '+rec.product_id.name))






    def check_imei_number_return_correct(self):
        order_product ={}
        imei_product ={}
        for rec in self.move_ids_without_package.filtered(lambda  p : p.product_id.product_tmpl_id.is_imei_required == True):
            order_product[rec.product_id.id] =rec.product_uom_qty
        for rec in self.imei_numbers_id:
            imei_product[rec.product_id.id] =  0.0
        for rec in self.imei_numbers_id:
            imei_product[rec.product_id.id] =  imei_product[rec.product_id.id]+1
        print(imei_product)
        print(order_product)
        for rec in self.move_ids_without_package.filtered(lambda  p : p.product_id.product_tmpl_id.is_imei_required == True):
            if imei_product == {}:
                raise UserError(_('Please enter IMEI Number'))
            if  imei_product ==   order_product:
                return;
            else:
                raise UserError(_('Please enter IMEI Number of Product '+rec.product_id.name))



    def check_is_it_return(self):
        return (self.picking_type_id.code == 'incoming') and (self.sale_id)

    def remove_from_imei_list(self):
        for rec in self.imei_numbers_id:
            imei = self.env['imei.number'].search([('name','=',rec.name),('product_id','=',rec.product_id.id)])
            if imei:
                pass
            else:
                return False
        else:
            return True
    def remove_lists_imei(self):

        for rec in self.imei_numbers_id:
            imei = self.env['imei.number'].search([('name','=',rec.name),('product_id','=',rec.product_id.id)])
            if imei:
                imei.unlink()
            else:
                raise UserError(_(rec.name+' does not exist for Product '+rec.product_id.name))





    def button_validate(self):
        self.ensure_one()
        temp =   super(StockPicking, self).button_validate()

        if self.check_is_it_return():
            self.check_imei_number_return_correct()
            self.remove_lists_imei()
        return  temp



