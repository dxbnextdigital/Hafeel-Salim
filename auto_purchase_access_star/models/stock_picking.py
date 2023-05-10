from odoo import models, fields, api, _

class Picking(models.Model):
    _inherit = 'stock.picking'
    transfer_to_next_digital = fields.Boolean(default=False)
    picking_type_code = fields.Selection(related="picking_type_id.code")
    make_invisible = fields.Boolean(compute="_compute_field_visible")
    po_ref = fields.Char()


    @api.depends('company_id','picking_type_code')
    def _compute_field_visible(self):
        print(self.company_id.id)
        if (self.company_id.id !=2):
            self.make_invisible = True
        else:
            self.make_invisible = False
            if (self.picking_type_code == 'outgoing'):
                self.make_invisible = False
            else:
                self.make_invisible = True



    @api.onchange('partner_id','picking_type_id')
    def change_transfer_status(self):
        self.ensure_one()
        print("yes")
        print(self.picking_type_code)
        print("""(self.company_id.id ==2) and (self.picking_type_code == 'outgoing')""",(self.company_id.id ==2) and (self.picking_type_code == 'outgoing'))
        if (self.company_id.id ==2) and (self.picking_type_code == 'outgoing'):
            if self.partner_id.id == 1:
                self.transfer_to_next_digital = True
            else :
                self.transfer_to_next_digital = False
        else:
            self.transfer_to_next_digital = False

    def button_validate(self):

       button_vaildate = super(Picking, self).button_validate()
       if self.transfer_to_next_digital and (self.company_id.id == 2) and (self.picking_type_code == 'outgoing') and not (self.po_ref):
            print('yes')
            purchase_order_id= self.env['purchase.order'].sudo().create({
            'company_id': 1,
            'partner_id': 7,
            'partner_ref': self.name ,
            'picking_type_id':1
            })
            for rec in self.move_ids_without_package:
                print(rec.read())
                vals = {
               'order_id': purchase_order_id.id,
               'product_id': rec.product_id.id,
               'product_qty': rec.product_qty
                }
                self.env['purchase.order.line'].sudo().create(vals)
            self.po_ref = purchase_order_id.sudo().name



       return button_vaildate

