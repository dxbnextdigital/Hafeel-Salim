from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ImeiReturnWiz(models.TransientModel):
    _name = 'imei.return.wiz'

    product_id = fields.Many2one('product.product', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    ret_product_quantity = fields.Integer()
    ret_imei_line_ids = fields.One2many('imei.return.wiz.line', 'ret_imei_id', string='Scanned IMEI')
    total_ret_imei = fields.Integer(compute='_compute_total_ret_imei', store=True)


    

    @api.depends('ret_imei_line_ids.is_return')
    def _compute_total_ret_imei(self):
        context = self._context
        move_id = self.env['stock.move'].browse(context.get('active_id'))
        total=[]
        for each in self:
            for value in each.ret_imei_line_ids:
                if value.is_return==True:
                    total.append(value)
                self.total_ret_imei = len(total)
                move_id.total_ret_imei = self.total_ret_imei

    
    def return_imei(self):
        context = self._context
        move_id = self.env['stock.move'].browse(context.get('active_id'))
        move_id.total_ret_imei = self.total_ret_imei
        product_imei_ids = self.env['product.imei'].search([('product_id', '=', move_id.product_id.id),
                                                            ('so_line_id','=',move_id.sale_line_id.id)]).unlink()
        for imei_line_id in self.ret_imei_line_ids:
            product_imei_id = self.env['product.imei'].create({'product_id': move_id.product_id.id,
                                                               'partner_id': move_id.sale_line_id.order_id.partner_id.id,
                                                               'user_id': move_id.sale_line_id.order_id.partner_id.user_id.id,
                                                               'team_id': move_id.sale_line_id.order_id.partner_id.team_id.id,
                                                               'product_barcode': move_id.product_id.barcode,
                                                               'product_brand': move_id.product_id.categ_id.id,
                                                               'order_date': move_id.sale_line_id.order_id.date_order,
                                                               'location_id': move_id.sale_line_id.order_id.custom_source_location_id.id,
                                                               'imei': imei_line_id.imei,
                                                               'so_id': move_id.sale_line_id.order_id.id,
                                                               'so_line_id': move_id.sale_line_id.id,
                                                               'invoice_id': move_id.sale_line_id.order_id.invoice_ids[0].id,
                                                               'invoice_date': move_id.sale_line_id.order_id.invoice_ids[0].invoice_date,
                                                               'is_return': imei_line_id.is_return})


class ImeiReturnWizLine(models.TransientModel):
    _name = 'imei.return.wiz.line'

    ret_imei_id = fields.Many2one('imei.return.wiz')
    imei = fields.Char()
    is_return = fields.Boolean(store=True)
