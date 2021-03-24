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


class SalesReport(models.TransientModel):
    _name = "wizard.sales.history"
    _description = "Current Sales History"

    #warehouse = fields.Many2many('stock.warehouse', 'wh_wiz_rel', 'wh', 'wiz', string='Warehouse', required=True)
    # category = fields.Many2many('product.category', 'categ_wiz_rel', 'categ', 'wiz', string='Warehouse')

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string="End Date", required=True)


    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)

    def export_xls(self):

        # objsales = self.env['sale.order'].search([('usage', '=', 'internal'), ('active', '=', True), ('company_id', 'in', self.warehouse.ids)], order='id')

        objsales = self.env['sale.order'].search([('date_order', '>=', self.start_date),
                                                               ('date_order', '<=', self.end_date), ('state', 'in', ('sale','done'))])

        salsids = tuple([sale_id.id for sale_id in objsales])

        date = datetime.now()
        report_name = 'sales_' + date.strftime("%y%m%d%H%M%S")
        date_string = date.strftime("%B-%y")
        filename = '%s %s' % (report_name, date_string)


        fp = io.BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf = {}

        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Sales Info')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        #sheet.merge_range(1, 7, 2, 10, 'Product Stock Info', format0)
        #sheet.merge_range(3, 7, 3, 10, comp, format11)

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


        objsalesln = self.env['sale.order.line'].search([('order_id', 'in', salsids)],order='id')

        rowno = 1
        colno = 0

        colno = 0
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Sl#', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Order Date', wbf['content_border_bg'])

        colno += 1
        column_width = 25
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Sales Person', wbf['content_border_bg'])


        colno += 1
        column_width = 35
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Partner Name', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Brand', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Barcode', wbf['content_border_bg'])

        colno += 1
        column_width = 65
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Product', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Analytic Tag', wbf['content_border_bg'])


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


            ################## Brand
            if (rec.product_id.brand.name in summary_brand):
                dic_brand = summary_brand[rec.product_id.brand.name]
                dic_brand['totalsale']=dic_brand['totalsale']+rec.price_subtotal
                dic_brand['noofqty'] = dic_brand['noofqty'] +rec.product_uom_qty
                #tmptotal = float(summary_brand[rec.product_id.brand.name]) + rec.price_subtotal
                summary_brand[rec.product_id.brand.name] = dic_brand #tmptotal
            else:
                dic_brand={}
                dic_brand= {'totalsale': rec.price_subtotal, 'noofqty': rec.product_uom_qty}
                summary_brand[rec.product_id.brand.name] = dic_brand #rec.price_subtotal


            colno = 0
            sheet.write(rowno, colno, rowno, wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.order_id.date_order.strftime('%d-%m-%Y')), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.salesman_id.name if rec.salesman_id.name else ""), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.order_id.partner_id.name if rec.order_id.partner_id.name else ""), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, rec.product_id.brand.name if rec.product_id.brand.name else "", wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.product_id.barcode if rec.product_id.barcode else ""), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, rec.product_id.name if rec.product_id.name else "", wbf['content_border'])

            colno += 1
            tagname=''
            for analytic_tag in rec.analytic_tag_ids:
                tagname += analytic_tag.name

            sheet.write(rowno, colno, tagname , wbf['content_border'])

            colno += 1
            sheet.write(rowno, colno, rec.product_id.standard_price, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, rec.price_unit, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, (rec.price_unit-rec.product_id.standard_price), wbf['content_float_border'])

            colno += 1
            sheet.write(rowno, colno, int(rec.product_uom_qty), wbf['content_int_border'])
            colno += 1
            sheet.write(rowno, colno, (rec.product_id.standard_price*rec.product_uom_qty), wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, (rec.price_subtotal), wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, ((rec.price_subtotal)-(rec.product_id.standard_price*rec.product_uom_qty)), wbf['content_float_border'])

            totcost =0.00
            totsal=0.00
            totqty=0

            rowno+=1
        sheet.merge_range(rowno, 0, rowno, 10, "Total", wbf['content_border_bg'])
        colno = 11
        sheet.write(rowno, colno, "=sum(L2:L"+str(rowno)+")", wbf['content_int_border_total'])
        colno = 12
        sheet.write(rowno, colno, "=sum(M2:M" + str(rowno) + ")", wbf['content_float_border_total'])
        colno = 13
        sheet.write(rowno, colno, "=sum(N2:N" + str(rowno) + ")", wbf['content_float_border_total'])
        colno = 14
        sheet.write(rowno, colno, "=sum(O2:O" + str(rowno) + ")", wbf['content_float_border_total'])
        rowno += 1

        # summary_by_salesperson = {}
        # summary_by_customer = {}
        # for so in objsales:


        ######################### Sales Person
        worksheet2 = workbook.add_worksheet('Sales Person Summary')

        colno = 0
        column_width = 30
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Sales Person Name', wbf['content_border_bg'])


        colno += 1
        column_width = 50
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Total Sales', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recsale in summary_sales_person:
            colno = 0
            worksheet2.write(rowno, colno, recsale, wbf['content_border'])
            colno += 1
            worksheet2.write(rowno, colno, summary_sales_person[recsale], wbf['content_float_border'])
            rowno += 1

        worksheet2.write(rowno, 0,  "Total", wbf['content_border_bg'])
        colno = 1
        worksheet2.write(rowno, colno, "=sum(B2:B" + str(rowno) + ")", wbf['content_float_border_total'])


        #######################################
        ########################Brand summary_brand[rec.product_id.brand.name]
        worksheet3 = workbook.add_worksheet('Brand Summary')

        colno = 0
        column_width = 50
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(0, colno, 'Brand', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(0, colno, 'No of Qty', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(0, colno, 'Total Sales', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recbrand in summary_brand:
            colno = 0
            worksheet3.write(rowno, colno, recbrand if recbrand else '', wbf['content_border'])
            colno += 1
            dic_sales = summary_brand[recbrand]
            worksheet3.write(rowno, colno, dic_sales['noofqty'], wbf['content_float_border'])
            colno += 1

            worksheet3.write(rowno, colno, dic_sales['totalsale'], wbf['content_float_border'])
            rowno += 1
        worksheet3.write(rowno, 0, "Total", wbf['content_border_bg'])
        colno = 1
        worksheet3.write(rowno, colno, "=sum(B2:B" + str(rowno) + ")", wbf['content_float_border_total'])
        colno += 1
        worksheet3.write(rowno, colno, "=sum(C2:C" + str(rowno) + ")", wbf['content_float_border_total'])

        ##############################################

        ########################Partner sales
        worksheet4 = workbook.add_worksheet('Customer Sales Summary')

        colno = 0
        column_width = 50
        worksheet4.set_column(colno, colno, column_width)
        worksheet4.write(0, colno, 'Customer Name', wbf['content_border_bg'])


        colno += 1
        column_width = 30
        worksheet4.set_column(colno, colno, column_width)
        worksheet4.write(0, colno, 'Total Sales', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recpartner in summary_partner:
            dic_partners = summary_partner[recpartner]
            colno = 0
            worksheet4.write(rowno, colno, dic_partners['partnername'] if dic_partners['partnername'] else '', wbf['content_border'])
            colno += 1
            worksheet4.write(rowno, colno, dic_partners['totalsale'], wbf['content_float_border'])
            rowno += 1
        worksheet4.write(rowno, 0, "Total", wbf['content_border_bg'])
        colno = 1
        worksheet4.write(rowno, colno, "=sum(B2:B" + str(rowno) + ")", wbf['content_float_border_total'])


        ##############################################


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
