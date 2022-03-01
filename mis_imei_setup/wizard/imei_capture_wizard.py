from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ImeiCaptureWiz(models.TransientModel):
    _name = 'imei.capture.wiz'

    product_id = fields.Many2one('product.product', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    product_quantity = fields.Integer()
    imei_line_ids = fields.One2many('imei.capture.wiz.line', 'imei_id', string='Scanned IMEI')
    total_imei = fields.Integer(compute='_compute_total_imei', store=True)

    @api.depends('imei_line_ids.imei')
    def _compute_total_imei(self):
        context = self._context
        so_line_id = self.env['sale.order.line'].browse(context.get('active_id'))
        total=[]
        for each in self:
            for value in each.imei_line_ids:
                total.append(value)
                self.total_imei = len(total)
                so_line_id.total_imei = self.total_imei
    
    def save_imei(self):
        context = self._context
        so_line_id = self.env['sale.order.line'].browse(context.get('active_id'))
        product_imei_ids = self.env['product.imei'].search([('product_id', '=', so_line_id.product_id.id),
                                                            ('so_line_id','=',so_line_id.id)]).unlink()
        for imei_line_id in self.imei_line_ids:
            product_imei_id = self.env['product.imei'].create({'product_id': so_line_id.product_id.id,
                                                               'product_barcode': so_line_id.product_id.barcode,
                                                               'product_brand': so_line_id.product_id.categ_id.id,
                                                               'location_id': so_line_id.order_id.custom_source_location_id.id,
                                                               'partner_id': so_line_id.order_id.partner_id.id,
                                                               'user_id': so_line_id.order_id.partner_id.user_id.id,
                                                               'team_id': so_line_id.order_id.partner_id.team_id.id,
                                                               'order_date': so_line_id.order_id.date_order,
                                                               'imei': imei_line_id.imei,
                                                               'so_id': so_line_id.order_id.id,
                                                               'so_line_id': so_line_id.id
                                                               })


class ImeiCaptureWizLine(models.TransientModel):
    _name = 'imei.capture.wiz.line'

    imei_id = fields.Many2one('imei.capture.wiz')
    imei = fields.Char(string='IMEI')
