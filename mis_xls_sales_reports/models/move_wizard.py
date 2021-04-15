import time
from datetime import date, datetime
import pytz
import json
import io
from odoo import api, fields, models, _
from odoo.tools import date_utils
import xlsxwriter
import base64
from datetime import timedelta
from odoo.exceptions import UserError

class SalesMoveReport(models.TransientModel):
    _name = "wizard.sales.move"
    _description = "Current Sales Move Report"

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string="End Date", required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    brand = fields.Many2one('mis.product.brand', string='Brand')
    product_id = fields.Many2one('product.product', string='Product')
    sales_person = fields.Many2one('res.users', string='Sales Person')

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)

    def _salesmanfilter(self):
        if self.sales_person:
            return ('user_id', '=', self.sales_person.id)
        else:
            return (1,'=',1)

    def _get_partner(self):
        if self.partner_id:
            return ('partner_id', '=', self.partner_id.id)
        else:
            return (1, '=', 1)

    def _domainfilter(self):
        return [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date), ('state', 'in', ('sale','done')),self._salesmanfilter(),
                self._get_partner()]

    def export_xls(self):
        objsales = self.env['sale.order'].search(self._domainfilter())
        salsids = tuple([sale_id.id for sale_id in objsales])
        date = datetime.now()
        report_name = 'move_' + date.strftime("%y%m%d%H%M%S")
        date_string = date.strftime("%B-%y")
        filename = '%s %s' % (report_name, date_string)

        fp = io.BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf = {}

        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Sales Info')
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')

        wbf['content_border'] = workbook.add_format()
        wbf['content_border'].set_top()
        wbf['content_border'].set_bottom()
        wbf['content_border'].set_left()
        wbf['content_border'].set_right()
        wbf['content_border'].set_text_wrap()

        wbf['content_border_red'] = workbook.add_format({'bg_color': 'red'})
        wbf['content_border_red'].set_top()
        wbf['content_border_red'].set_bottom()
        wbf['content_border_red'].set_left()
        wbf['content_border_red'].set_right()
        wbf['content_border_red'].set_text_wrap()

        wbf['content_border_bg'] = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'bold': 1, 'bg_color': '#E1E1E1'})
        wbf['content_border_bg'].set_top()
        wbf['content_border_bg'].set_bottom()
        wbf['content_border_bg'].set_left()
        wbf['content_border_bg'].set_right()
        wbf['content_border_bg'].set_text_wrap()

        wbf['content_float_border'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00'})
        wbf['content_float_border'].set_top()
        wbf['content_float_border'].set_bottom()
        wbf['content_float_border'].set_left()
        wbf['content_float_border'].set_right()

        wbf['content_int_border'] = workbook.add_format({'align': 'right', 'num_format': '#,##0'})
        wbf['content_int_border'].set_top()
        wbf['content_int_border'].set_bottom()
        wbf['content_int_border'].set_left()
        wbf['content_int_border'].set_right()

        wbf['content_float_border_total'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00', 'bold': 1, 'bg_color': '#E1E1E1'})
        wbf['content_float_border_total'].set_top()
        wbf['content_float_border_total'].set_bottom()
        wbf['content_float_border_total'].set_left()
        wbf['content_float_border_total'].set_right()


        wbf['content_int_border_total'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', 'bold': 1, 'bg_color': '#E1E1E1'})
        wbf['content_int_border_total'].set_top()
        wbf['content_int_border_total'].set_bottom()
        wbf['content_int_border_total'].set_left()
        wbf['content_int_border_total'].set_right()

        objlocation = self.env['stock.location'].search(
            [('usage', '=', 'internal'), ('active', '=', True), ('company_id', '=', 1)], order='id')

        locationids = tuple([loc_id.id for loc_id in objlocation])



        summary_sol = {}
        if self.product_id and self.brand:
            objsalesln = self.env['sale.order.line'].search([('order_id', 'in', salsids),
                                                             ('product_id', '=', self.product_id.id),
                                                             ('product_id.brand', '=', self.brand.id)
                                                             ], order='id')
        elif self.product_id:
            objsalesln = self.env['sale.order.line'].search([('order_id', 'in', salsids),
                                                             ('product_id', '=', self.product_id.id)
                                                             ], order='id')
        elif self.brand:
            objsalesln = self.env['sale.order.line'].search([('order_id', 'in', salsids),
                                                             ('product_id.brand', '=', self.brand.id)
                                                             ],order='id')
        else:
            objsalesln = self.env['sale.order.line'].search([('order_id', 'in', salsids)],order='id')

        for sol in objsalesln:
            if (sol.product_id.id in summary_sol):
                dic_product = summary_sol[sol.product_id.id]
                dic_sales_location = dic_product['sale_loc']

                if sol.order_id.custom_source_location_id.id in dic_sales_location:
                    lid =sol.order_id.custom_source_location_id.id

                    dicsalloc=dic_sales_location[lid]

                    dicsalloc['qty'] = dicsalloc['qty']+sol.product_uom_qty
                    dicsalloc['price_unit'] = dicsalloc['price_unit']+sol.price_unit
                    dicsalloc['price_subtotal'] = dicsalloc['price_subtotal']+sol.price_subtotal
                    dicsalloc['price_total'] = dicsalloc['price_total']+sol.price_total
                    dicsalloc['margin'] = dicsalloc['margin']+sol.margin
                    #raise UserError(str(priqty) + ' ======== '  + str(dicsalloc['qty']))
                    dic_sales_location[lid]=dicsalloc
                dic_product['price_unit']=dic_product['price_unit'] + sol.price_unit*sol.product_uom_qty
                dic_product['qty'] = dic_product['qty'] + sol.product_uom_qty
                dic_product['price_subtotal'] = dic_product['price_subtotal'] + sol.price_subtotal
                dic_product['margin'] = dic_product['margin'] + sol.margin
                dic_product['price_total'] = dic_product['price_total'] + sol.price_total
                dic_product['sale_loc'] = dic_sales_location
                summary_sol[sol.product_id.id] = dic_product
            else:
                sale_location = {}

                for loc in objlocation:
                    dic_location = {
                        'location_id': loc.id,
                        'location_name': loc.name,
                        'qty': 0,
                        'price_unit': 0.0,
                        'price_subtotal': 0.0,
                        'price_total': 0.0,
                        'margin': 0.0
                    }
                    sale_location[loc.id] = dic_location

                dic_sales_location = sale_location
                if sol.order_id.custom_source_location_id.id in dic_sales_location:
                    lid = sol.order_id.custom_source_location_id.id
                    dicsalloc = dic_sales_location[lid]
                    dicsalloc['qty'] = sol.product_uom_qty
                    dicsalloc['price_unit'] =  sol.price_unit
                    dicsalloc['price_subtotal'] = sol.price_subtotal
                    dicsalloc['price_total'] =  sol.price_total
                    dicsalloc['margin'] = sol.margin
                    dic_sales_location[lid] = dicsalloc

                dic_product= {'product_id': sol.product_id, 'qty': sol.product_uom_qty,
                              'price_unit': sol.price_unit,
                              'price_subtotal': sol.price_subtotal,
                              'price_total': sol.price_total,
                              'margin': sol.margin,
                              'sale_loc':dic_sales_location,
                              }
                summary_sol[sol.product_id.id] = dic_product

        rowno = 1
        colno = 0

        colno = 0
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Sl#', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Brand', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Barcode', wbf['content_border_bg'])

        colno += 1
        column_width = 65
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Product', wbf['content_border_bg'])


        colno += 1
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Cost', wbf['content_border_bg'])

        colno += 1
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Sales Price', wbf['content_border_bg'])

        colno += 1
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Unit Profit', wbf['content_border_bg'])

        colno += 1
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'QTY', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Total Cost', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Total Sales Price', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Total Profit', wbf['content_border_bg'])

        for locid in sale_location:
            diclocation=sale_location[locid]
            colno += 1
            column_width = 15
            sheet.set_column(colno, colno, column_width)
            sheet.write(rowno - 1, colno, diclocation['location_name'], wbf['content_border_bg'])
            colno += 1
            column_width = 15
            sheet.set_column(colno, colno, column_width)
            sheet.write(rowno - 1, colno, diclocation['location_name'] + "- Total Cost", wbf['content_border_bg'])
            colno += 1
            column_width = 15
            sheet.set_column(colno, colno, column_width)
            sheet.write(rowno - 1, colno, diclocation['location_name'] + " - Total Sale Price", wbf['content_border_bg'])
            colno += 1
            column_width = 15
            sheet.set_column(colno, colno, column_width)
            sheet.write(rowno - 1, colno, diclocation['location_name'] + ' - Total Margin' , wbf['content_border_bg'])

        summary_sales_person = {}
        summary_brand = {}
        summary_partner = {}

        for rec in objsalesln:
            if (rec.salesman_id.name in summary_sales_person):
                tmptotal = float(summary_sales_person[rec.salesman_id.name]) + rec.price_subtotal
                summary_sales_person[rec.salesman_id.name] = tmptotal
            else:
                summary_sales_person[rec.salesman_id.name] = rec.price_subtotal

            #################### Partner
            if (rec.order_id.partner_id.id in summary_partner):
                dic_partner = summary_partner[rec.order_id.partner_id.id]
                dic_partner['totalsale']=dic_partner['totalsale']+rec.price_subtotal
                summary_partner[rec.order_id.partner_id.id] = dic_partner
            else:
                dic_partner={}
                dic_partner= {'partnername': rec.order_id.partner_id.name, 'totalsale': rec.price_subtotal}
                summary_partner[rec.order_id.partner_id.id] = dic_partner
        rowno += 1
        for proid in summary_sol:
            dic_prod = summary_sol[proid]

            dicsalelocation =dic_prod['sale_loc']
            colno = 0
            sheet.write(rowno - 1, colno, rowno-1, wbf['content_border'])
            colno += 1
            sheet.write(rowno - 1, colno, dic_prod['product_id'].brand.name, wbf['content_border'])
            colno += 1
            barcode =''
            if dic_prod['product_id'].barcode:
                barcode=dic_prod['product_id'].barcode
            sheet.write(rowno - 1, colno, barcode, wbf['content_border'])
            colno += 1
            sheet.write(rowno - 1, colno, dic_prod['product_id'].name, wbf['content_border'])
            colno += 1
            sheet.write(rowno - 1, colno, dic_prod['product_id'].standard_price, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno - 1, colno, (dic_prod['price_unit']/ dic_prod['qty'] if dic_prod['qty']>0 else 1), wbf['content_float_border'])
            colno += 1
            sheet.write(rowno - 1, colno, (dic_prod['margin']/ dic_prod['qty'] if dic_prod['qty']>0 else 1), wbf['content_float_border'])
            colno += 1
            sheet.write(rowno - 1, colno, dic_prod['qty'], wbf['content_int_border'])
            colno += 1
            sheet.write(rowno - 1,colno, (dic_prod['product_id'].standard_price* dic_prod['qty']), wbf['content_float_border'])
            colno += 1
            sheet.write(rowno - 1, colno, dic_prod['price_unit'], wbf['content_float_border'])
            colno += 1
            sheet.write(rowno - 1, colno, dic_prod['margin'], wbf['content_float_border'])

            for loid in dicsalelocation:
                diclocsale = dicsalelocation[loid]
                colno += 1
                sheet.write(rowno - 1, colno, diclocsale['qty'], wbf['content_int_border'])
                colno += 1
                sheet.write(rowno - 1, colno, dic_prod['product_id'].standard_price * diclocsale['qty'],
                            wbf['content_int_border'])
                colno += 1
                sheet.write(rowno - 1, colno, diclocsale['price_total'], wbf['content_int_border'])
                colno += 1
                sheet.write(rowno - 1, colno, diclocsale['margin'], wbf['content_int_border'])
            rowno += 1

        rowno -= 1
        sheet.merge_range(rowno, 0, rowno, 6, "Total", wbf['content_border_bg'])
        colno = 7
        sheet.write(rowno, colno, "=sum(H2:H" + str(rowno) + ")", wbf['content_float_border_total'])
        colno += 1
        sheet.write(rowno, colno, "=sum(I2:I" + str(rowno) + ")", wbf['content_float_border_total'])
        colno += 1
        sheet.write(rowno, colno, "=sum(J2:J" + str(rowno) + ")", wbf['content_float_border_total'])
        colno += 1
        sheet.write(rowno, colno, "=sum(K2:K" + str(rowno) + ")", wbf['content_float_border_total'])
        total_col = colno
        colno =  total_col
        for loid in objlocation:
            colno += 1
            letter= ''
            if (65+colno)>90:
                letter='A' + str(chr(39+colno))
            else:
                letter = str(chr(65 + colno))

            sheet.write(rowno, colno, "=sum(" + letter+ "2:" + letter+   str(rowno) + ")", wbf['content_float_border_total'])
            colno += 1

            if (65+colno)>90:
                letter='A' + str(chr(39+colno))
            else:
                letter = str(chr(65 + colno))


            sheet.write(rowno, colno, "=sum(" + letter + "2:" + letter + str(rowno) + ")",
                        wbf['content_float_border_total'])
            colno += 1
            if (65+colno)>90:
                letter='A' + str(chr(39+colno))
            else:
                letter = str(chr(65 + colno))

            sheet.write(rowno, colno, "=sum(" + letter + "2:" + letter + str(rowno) + ")",
                        wbf['content_float_border_total'])
            colno += 1
            if (65+colno)>90:
                letter='A' + str(chr(39+colno))
            else:
                letter = str(chr(65 + colno))

            sheet.write(rowno, colno, "=sum(" + letter + "2:" + letter + str(rowno) + ")",
                        wbf['content_float_border_total'])
            #raise UserError("=sum(" + chr(65 + colno) + "2:" + chr(65 + colno) + str(rowno) + ")")

        workbook.close()
        out = base64.encodestring(fp.getvalue())
        self.write({'datas': out, 'datas_fname': filename})
        fp.close()
        filename += '%2Exlsx'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'web/content/?model=' + self._name + '&id=' + str(
                self.id) + '&field=datas&download=true&filename=' + filename,
        }
