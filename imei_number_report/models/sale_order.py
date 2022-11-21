from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def chunkIt(self,seq, num):
        # looping till length l
            for i in range(0, len(seq), num):
                yield seq[i:i + num]
    def get_details_imei(self):
        data ={}

        for rec in self.imei_numbers_id:
            data[rec.product_id.name] = []
        for rec in self.imei_numbers_id:
            temp =data[rec.product_id.name]
            temp.append(rec.name)
            data[rec.product_id.name] = temp
        new_list = []
        for key, val in data.items():
            new_list.append([key, self.chunkIt(val,5)])


        print(new_list)
        return new_list

class AccountMove(models.Model):
    _inherit = 'account.move'
    sale_id = fields.Many2one('sale.order',compute='_compute_sale_order')

    def _compute_sale_order(self):
        temp = self.env['sale.order'].search([('invoice_ids', 'in', [self.id])],limit=1)
        self.sale_id =temp


    def get_data_from(self):
        print(self.id)
        invoice_id = self.id
        temp = self.env['sale.order'].search([('invoice_ids', 'in', [invoice_id])],limit=1)
        print(temp)

        return temp.get_details_imei()