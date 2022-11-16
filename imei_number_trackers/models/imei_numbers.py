from odoo import fields, models, api,_
from odoo.exceptions import Warning, UserError, ValidationError


class ImeiNumbers(models.Model):
    _name = 'imei.number'
    _description = 'Description'
    _sql_constraints = [('name', 'unique(name)', 'IMEI should be Unique')]


    name = fields.Char(required=True)
    sale_order = fields.Many2one('sale.order')
    product_id = fields.Many2one('product.product')
    account_move_id = fields.Many2one('account.move', string='Invoice' ,compute ='_compute_invoice')
    partner_id = fields.Many2one('res.partner',related='sale_order.partner_id',store=True)

    # invoice_id = fields.Many2one('account.move', string='Invoice No')
    invoice_date = fields.Date(string='Invoice Date')
    product_barcode = fields.Char(string='Product Barcode' , related='product_id.barcode',store=True)
    # product_id = fields.Many2one('product.product', string='Product')
    product_brand = fields.Many2one('mis.product.brand', related='product_id.brand', string='Product Brand',store=True)
    # is_return = fields.Boolean(string='Return')
    # so_id = fields.Many2one('sale.order', string='Sale Order')
    user_id = fields.Many2one('res.users', string='Sales Executive',related='sale_order.user_id',store=True)
    team_id = fields.Many2one('crm.team', string='Sales Team',related='sale_order.team_id',store=True)
    location_id = fields.Many2one('stock.location', string='Location', related='sale_order.custom_source_location_id',store=True)
    order_date = fields.Datetime(string='Order Date',related='sale_order.date_order',store=True)

    @api.depends('sale_order')
    def _compute_invoice(self):
        self.account_move_id = False
        for rec in self.sale_order.invoice_ids:
            self.account_move_id = rec.id
            self.invoice_date = rec.invoice_date
            break
    @api.constrains('name')
    def _check_date_end(self):
        imei_number = self.name
        print(imei_number.isnumeric())
        if (imei_number.isnumeric()):
            if len(imei_number) == 15:
                    pass
            else:
                raise UserError(_('Required IMEI Number 15 digit'))
        else:
            raise UserError(_('IMEI Number should be Number '))

    def create_record(self,name,sale_order,product_id):
        result= self.env['imei.number'].sudo().create({
            'name' :str(name),
            'sale_order': int(sale_order),
            'product_id': int(product_id)

        }).read()

        result[0]['product_id']=[product_id]
        print(result)

        return result[0]







    def edit_sale_imei_number(self,id,name):
        record = self.env['imei.number'].search([('id','=',id)])
        print(record)
        record.write({'name':name})
        result = record.read()
        result[0]['product_id'] = [record.product_id.id]
        print(result)
        return result[0]

    def imei_remove_imei(self,id):
        self.env['imei.number'].search([('id','=',id)]).unlink()