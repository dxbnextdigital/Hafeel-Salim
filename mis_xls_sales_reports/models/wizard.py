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
        sheet.write(rowno-1, colno, 'QTY', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Total Cost', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Total Sales Price', wbf['content_border_bg'])

        for rec in objsalesln:

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
            sheet.write(rowno, colno, rec.product_id.standard_price, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, rec.product_id.list_price, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, rec.product_uom_qty, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, (rec.product_id.standard_price*rec.product_uom_qty), wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, (rec.product_id.list_price*rec.product_uom_qty), wbf['content_float_border'])

            totcost =0.00
            totsal=0.00
            totqty=0

            rowno+=1
        sheet.merge_range(rowno, 0, rowno, 8, "Total", wbf['content_border_bg'])
        colno = 9
        sheet.write(rowno, colno, "=sum(J2:J"+str(rowno)+")", wbf['content_float_border'])
        colno = 10
        sheet.write(rowno, colno, "=sum(K2:K" + str(rowno) + ")", wbf['content_float_border'])
        colno = 11
        sheet.write(rowno, colno, "=sum(L2:L" + str(rowno) + ")", wbf['content_float_border'])
        rowno += 1

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
