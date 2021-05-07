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


class CreditNoteReport(models.TransientModel):
    _name = "wizard.creditnote.history"
    _description = "Current CreditNote History"


    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string="End Date", required=True)


    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)


    def export_xls(self):


        objinvoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date),
                                                      ('invoice_date', '<=', self.end_date), ('state', '=', 'posted'),
                                                    ('move_type', '=', 'out_refund')])

        date = datetime.now()
        report_name = 'creditnote_' + date.strftime("%y%m%d%H%M%S")
        date_string = date.strftime("%B-%y")
        filename = '%s %s' % (report_name, date_string)

        fp = io.BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        wbf = {}

        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Creditnote Info')
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


        rowno = 1
        colno = 0

        colno = 0
        column_width = 10
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Sl#', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Invoice No', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Invoice Date', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Due on', wbf['content_border_bg'])

        colno += 1
        column_width = 25
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Sales Person', wbf['content_border_bg'])

        colno += 1
        column_width = 60
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Partner Name', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Total Amount', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno-1, colno, 'Due Amount', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        sheet.set_column(colno, colno, column_width)
        sheet.write(rowno - 1, colno, 'Paid', wbf['content_border_bg'])

        summary_sales_person = {}
        summary_partner = {}
        summary_product = {}
        for rec in objinvoice:
            objline = self.env['account.move.line'].search([('move_id', '=', rec.id),
                                                      ('product_id', '!=', False)])
            for recln in objline:
                #raise UserError(recln.product_id.id)
                if (recln.product_id.id in summary_product):
                    #raise UserError(recln.product_id.id)
                    dic_product= summary_product[recln.product_id.id]
                    dic_product['price_unit']+=recln.price_unit
                    dic_product['qty'] += recln.quantity
                    dic_product['price_subtotal'] += recln.price_subtotal
                    dic_product['price_total'] += recln.price_total
                    summary_product[recln.product_id.id] =dic_product
                else:
                    dic_product = {'product_id': recln.product_id, 'qty': recln.quantity,
                                   'price_unit': recln.price_unit,
                                   'price_subtotal': recln.price_subtotal,
                                   'price_total': recln.price_total,
                                   }
                    summary_product[recln.product_id.id] = dic_product
            ####################### Sales Person Due Report
            if (rec.invoice_user_id.name in summary_sales_person):
                dic_salesperson = summary_sales_person[rec.invoice_user_id.name]
                dic_sp_product = dic_salesperson['product']
                for recln in objline:
                    if (recln.product_id.id in dic_sp_product):
                        dic_product = dic_sp_product[recln.product_id.id]
                        dic_product['price_unit'] += recln.price_unit
                        dic_product['qty'] += recln.quantity
                        dic_product['price_subtotal'] += recln.price_subtotal
                        dic_product['price_total'] += recln.price_total
                        dic_sp_product[recln.product_id.id]=dic_product
                    else:
                        dic_product = {'product_id': recln.product_id, 'qty': recln.quantity,
                                          'price_unit': recln.price_unit,
                                          'price_subtotal': recln.price_subtotal,
                                          'price_total': recln.price_total,
                                          }
                        dic_sp_product[recln.product_id.id] = dic_product

                dic_salesperson['product'] = dic_sp_product
                dic_salesperson['totalinvoice'] = dic_salesperson['totalinvoice'] + rec.amount_total_signed
                dic_salesperson['totaldue'] = dic_salesperson['totaldue'] + rec.amount_residual_signed
                summary_sales_person[rec.invoice_user_id.name] = dic_salesperson
            else:
                dic_sp_product1={}
                for recln in objline:
                    if (recln.product_id.id in dic_sp_product1):
                        dic_product1 = dic_sp_product1[recln.product_id.id]
                        dic_product1['price_unit'] += recln.price_unit
                        dic_product1['qty'] += recln.quantity
                        dic_product1['price_subtotal'] += recln.price_subtotal
                        dic_product1['price_total'] += recln.price_total
                        dic_sp_product1[recln.product_id.id] = dic_product1
                    else:
                        dic_product1 = {'product_id': recln.product_id, 'qty': recln.quantity,
                                       'price_unit': recln.price_unit,
                                       'price_subtotal': recln.price_subtotal,
                                       'price_total': recln.price_total,
                                       }
                        dic_sp_product1[recln.product_id.id] = dic_product1

                dic_salesperson = {'totalinvoice': rec.amount_total_signed, 'totaldue': rec.amount_residual_signed,
                                   'product' : dic_sp_product1}
                summary_sales_person[rec.invoice_user_id.name] = dic_salesperson

            ####################### Partner Due Report
            if (rec.partner_id.id in summary_partner):
                dic_partner = summary_partner[rec.partner_id.id]
                dic_partner['totalinvoice'] = dic_partner['totalinvoice'] + rec.amount_total_signed
                dic_partner['totaldue'] = dic_partner['totaldue'] + rec.amount_residual_signed
                summary_partner[rec.partner_id.id] = dic_partner
            else:
                dic_partner = {}
                dic_partner = {'partnername': rec.partner_id.name, 'totalinvoice': rec.amount_total_signed, 'totaldue': rec.amount_residual_signed}
                summary_partner[rec.partner_id.id] = dic_partner


            #################################

            colno = 0
            sheet.write(rowno, colno, rowno, wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.name if rec.name else ""), wbf['content_border'])

            colno += 1
            sheet.write(rowno, colno, str(rec.invoice_date.strftime('%d-%m-%Y')), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.invoice_payment_term_id.name if rec.invoice_payment_term_id.name else ""), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, str(rec.invoice_user_id.name if rec.invoice_user_id.name else ""), wbf['content_border'])
            colno += 1
            sheet.write(rowno, colno, rec.partner_id.name if rec.partner_id.name else "", wbf['content_border'])

            colno += 1
            sheet.write(rowno, colno, rec.amount_total_signed, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, rec.amount_residual_signed, wbf['content_float_border'])
            colno += 1
            sheet.write(rowno, colno, ((rec.amount_total_signed)-(rec.amount_residual_signed)), wbf['content_float_border'])

            rowno+=1
        sheet.merge_range(rowno, 0, rowno, 5, "Total", wbf['content_border_bg'])
        colno = 6
        sheet.write(rowno, colno, "=sum(G2:G"+str(rowno)+")", wbf['content_float_border_total'])
        colno = 7
        sheet.write(rowno, colno, "=sum(H2:H" + str(rowno) + ")", wbf['content_float_border_total'])
        colno = 8
        sheet.write(rowno, colno, "=sum(I2:I" + str(rowno) + ")", wbf['content_float_border_total'])
        rowno += 1
        #####################################  Credit Note by product

        worksheet2 = workbook.add_worksheet('By Product')

        colno = 0
        column_width = 20
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Barode', wbf['content_border_bg'])

        colno += 1
        column_width = 100
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Product Name', wbf['content_border_bg'])
        colno += 1
        column_width = 15
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Qty', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Unit Price', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet2.set_column(colno, colno, column_width)
        worksheet2.write(0, colno, 'Total Price', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recproduct in summary_product:
            dic_pro = summary_product[recproduct]
            colno = 0
            worksheet2.write(rowno, colno, dic_pro['product_id'].barcode, wbf['content_border'])
            colno += 1
            worksheet2.write(rowno, colno, dic_pro['product_id'].name, wbf['content_border'])
            colno += 1
            worksheet2.write(rowno, colno, dic_pro['qty'], wbf['content_int_border'])
            colno += 1
            worksheet2.write(rowno, colno, dic_pro['price_total'] / dic_pro['qty'] if dic_pro['qty'] else 1, wbf['content_float_border'])
            colno += 1
            worksheet2.write(rowno, colno, dic_pro['price_total'], wbf['content_float_border'])
            rowno += 1

        worksheet2.merge_range(rowno, 0, rowno, 1, "Total", wbf['content_border_bg'])
        colno = 2
        worksheet2.write(rowno, colno, "=sum(C2:C" + str(rowno) + ")", wbf['content_int_border_total'])
        colno += 1
        worksheet2.write(rowno, colno, "", wbf['content_float_border_total'])
        colno += 1
        worksheet2.write(rowno, colno, "=sum(E2:E" + str(rowno) + ")", wbf['content_float_border_total'])

        #####################################  Sales Person
        worksheet4 = workbook.add_worksheet('Sales Person Summary')

        colno = 0
        column_width = 50
        worksheet4.set_column(colno, colno, column_width)
        worksheet4.write(0, colno, 'Sales Person Name', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet4.set_column(colno, colno, column_width)
        worksheet4.write(0, colno, 'Total Invoice', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet4.set_column(colno, colno, column_width)
        worksheet4.write(0, colno, 'Total Due', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recseleperson in summary_sales_person:

            colno = 0
            worksheet4.write(rowno, colno, recseleperson if recseleperson else '', wbf['content_border'])
            colno += 1
            dic_sales_persons = summary_sales_person[recseleperson]
            worksheet4.write(rowno, colno, dic_sales_persons['totalinvoice'], wbf['content_float_border'])
            colno += 1

            worksheet4.write(rowno, colno, dic_sales_persons['totaldue'], wbf['content_float_border'])
            rowno += 1
        worksheet4.write(rowno, 0, "Total", wbf['content_border_bg'])
        colno = 1
        worksheet4.write(rowno, colno, "=sum(B2:B" + str(rowno) + ")", wbf['content_float_border_total'])
        colno += 1
        worksheet4.write(rowno, colno, "=sum(C2:C" + str(rowno) + ")", wbf['content_float_border_total'])

        #####################################  product by Sales Person

        worksheet5 = workbook.add_worksheet('Product  By Sales Person')

        colno = 0
        column_width = 30
        worksheet5.set_column(colno, colno, column_width)
        worksheet5.write(0, colno, 'Sales Person Name', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        worksheet5.set_column(colno, colno, column_width)
        worksheet5.write(0, colno, 'Barode', wbf['content_border_bg'])

        colno += 1
        column_width = 100
        worksheet5.set_column(colno, colno, column_width)
        worksheet5.write(0, colno, 'Product Name', wbf['content_border_bg'])
        colno += 1
        column_width = 15
        worksheet5.set_column(colno, colno, column_width)
        worksheet5.write(0, colno, 'Qty', wbf['content_border_bg'])

        colno += 1
        column_width = 15
        worksheet5.set_column(colno, colno, column_width)
        worksheet5.write(0, colno, 'Unit Price', wbf['content_border_bg'])

        colno += 1
        column_width = 20
        worksheet5.set_column(colno, colno, column_width)
        worksheet5.write(0, colno, 'Total Price', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recseleperson in summary_sales_person:


            dic_sales_persons = summary_sales_person[recseleperson]
            dic_pro=dic_sales_persons["product"]
            for recproduct in summary_product:
                colno = 0
                worksheet5.write(rowno, colno, recseleperson if recseleperson else '', wbf['content_border'])
                dic_pro = summary_product[recproduct]
                colno += 1
                worksheet5.write(rowno, colno, dic_pro['product_id'].barcode, wbf['content_border'])
                colno += 1
                worksheet5.write(rowno, colno, dic_pro['product_id'].name, wbf['content_border'])
                colno += 1
                worksheet5.write(rowno, colno, dic_pro['qty'], wbf['content_int_border'])
                colno += 1
                worksheet5.write(rowno, colno, dic_pro['price_total'] / dic_pro['qty'] if dic_pro['qty'] else 1, wbf['content_float_border'])
                colno += 1
                worksheet5.write(rowno, colno, dic_pro['price_total'], wbf['content_float_border'])
                rowno += 1

        worksheet5.merge_range(rowno, 0, rowno, 2, "Total", wbf['content_border_bg'])
        colno = 3
        worksheet5.write(rowno, colno, "=sum(D2:d" + str(rowno) + ")", wbf['content_int_border_total'])
        colno += 1
        worksheet5.write(rowno, colno, "", wbf['content_float_border_total'])
        colno += 1
        worksheet5.write(rowno, colno, "=sum(F2:F" + str(rowno) + ")", wbf['content_float_border_total'])

        ########################Partner sales
        worksheet3 = workbook.add_worksheet('Customer wise Summary')

        colno = 0
        column_width = 50
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(0, colno, 'Customer Name', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(0, colno, 'Total Invoice', wbf['content_border_bg'])

        colno += 1
        column_width = 30
        worksheet3.set_column(colno, colno, column_width)
        worksheet3.write(0, colno, 'Total Due', wbf['content_border_bg'])

        rowno = 1
        colno = 0
        for recpartner in summary_partner:
            dic_partners = summary_partner[recpartner]
            colno = 0
            worksheet3.write(rowno, colno, dic_partners['partnername'] if dic_partners['partnername'] else '',
                             wbf['content_border'])
            colno += 1
            worksheet3.write(rowno, colno, dic_partners['totalinvoice'], wbf['content_float_border'])

            colno += 1
            worksheet3.write(rowno, colno, dic_partners['totaldue'], wbf['content_float_border'])
            rowno += 1
        worksheet3.write(rowno, 0, "Total", wbf['content_border_bg'])
        colno = 1
        worksheet3.write(rowno, colno, "=sum(B2:B" + str(rowno) + ")", wbf['content_float_border_total'])
        colno += 1
        worksheet3.write(rowno, colno, "=sum(C2:C" + str(rowno) + ")", wbf['content_float_border_total'])

        ###############################

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
