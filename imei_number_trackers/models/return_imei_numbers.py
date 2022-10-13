from odoo import fields, models, api,_
from odoo.exceptions import Warning, UserError, ValidationError


class ImeiNumberReturn(models.Model):
    _name = 'imei.number.return'

    product_id = fields.Many2one('product.product')
    name = fields.Char(required=True,string='IMEI Number')
    picking_id = fields.Many2one('stock.picking')
    account_move_id = fields.Many2one('account.move', string='Invoice' ,compute ='_compute_invoice')
    partner_id = fields.Many2one('res.partner',related='sale_order.partner_id',store=True)

    sale_order = fields.Many2one('sale.order',related='picking_id.sale_id',store=True)
    invoice_date = fields.Date(string='Invoice Date', related='account_move_id.invoice_date')
    product_barcode = fields.Char(string='Product Barcode', related='product_id.barcode',store=True)
    # product_id = fields.Many2one('product.product', string='Product')
    product_brand = fields.Many2one('mis.product.brand', related='product_id.brand', string='Product Brand',store=True)
    # is_return = fields.Boolean(string='Return')
    # so_id = fields.Many2one('sale.order', string='Sale Order')
    user_id = fields.Many2one('res.users', string='Sales Executive', related='sale_order.user_id',store=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', related='sale_order.team_id',store=True)
    location_id = fields.Many2one('stock.location', string='Location', related='sale_order.custom_source_location_id',store=True)
    order_date = fields.Datetime(string='Order Date', related='sale_order.date_order',store=True)
    state_of_imei = fields.Selection(related='picking_id.state')

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
        if (imei_number.isnumeric()):
            if len(imei_number) == 15:
                pass
            else:
                raise UserError(_('Required IMEI Number 15 digit'))
        else:
            raise UserError(_('IMEI Number should be Number '))

    def get_return_imei(self,id):

        return self.env['imei.number.return'].search_read([('picking_id','=',id)])

    def create_record(self,name,picking_id,product_id):
        print(picking_id)
        print(product_id)
        result = self.env['imei.number.return'].sudo().create({
            'name': str(name),
            'picking_id': int(picking_id),
            'product_id': int(product_id)

        }).read()
        result[0]['product_id'] = [product_id]
        print(result)

        return result[0]

    def imei_remove_imei(self,id):
        print(id)
        print("ssss",self.env['imei.number.return'].search([('id','=',id)]))
        self.env['imei.number.return'].search([('id','=',id)]).unlink()
