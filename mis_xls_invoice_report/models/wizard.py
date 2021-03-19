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


class InvoiceReport(models.TransientModel):
    _name = "wizard.invoice.history"
    _description = "Current Invoice History"

    start_date = fields.Date(string='Start Date', required="1")
    end_date = fields.Date(string="End Date", required="1")


    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonly=True)


    def export_xls(self):


        objinvoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date),
                                                               ('invoice_date', '<=', self.end_date), ('state', '=', 'posted'),
                                                    ('move_type', '=', 'out_invoice'), ('amount_residual_signed', '>', 0.0)])



        date = datetime.now()
        report_name = 'invoice_' + date.strftime("%y%m%d%H%M%S")
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

        for rec in objinvoice:
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
        sheet.write(rowno, colno, "=sum(G2:G"+str(rowno)+")", wbf['content_int_border_total'])
        colno = 7
        sheet.write(rowno, colno, "=sum(H2:H" + str(rowno) + ")", wbf['content_float_border_total'])
        colno = 8
        sheet.write(rowno, colno, "=sum(I2:I" + str(rowno) + ")", wbf['content_float_border_total'])

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
    #
    # def export_detail_xls(self):
    #
    #     objinvoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date),
    #                                                   ('invoice_date', '<=', self.end_date), ('state', '=', 'posted'),
    #                                                   ('move_type', '=', 'out_invoice'),
    #                                                   ('amount_residual_signed', '>', 0.0)])
    #
    #     invoiceids = tuple([invoice_id.id for invoice_id in objinvoice])
    #
    #     date = datetime.now()
    #     report_name = 'invoice_' + date.strftime("%y%m%d%H%M%S")
    #     date_string = date.strftime("%B-%y")
    #     filename = '%s %s' % (report_name, date_string)
    #
    #     fp = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(fp)
    #     wbf = {}
    #
    #     comp = self.env.user.company_id.name
    #     sheet = workbook.add_worksheet('Sales Info')
    #     format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
    #     format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
    #     format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
    #     format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
    #     format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
    #     format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
    #     font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
    #     font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
    #     font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
    #     red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
    #     justify = workbook.add_format({'font_size': 12})
    #     format3.set_align('center')
    #     justify.set_align('justify')
    #     format1.set_align('center')
    #     red_mark.set_align('center')
    #
    #     wbf['content_border'] = workbook.add_format()
    #     wbf['content_border'].set_top()
    #     wbf['content_border'].set_bottom()
    #     wbf['content_border'].set_left()
    #     wbf['content_border'].set_right()
    #     wbf['content_border'].set_text_wrap()
    #
    #     wbf['content_border_red'] = workbook.add_format({'bg_color': 'red'})
    #     wbf['content_border_red'].set_top()
    #     wbf['content_border_red'].set_bottom()
    #     wbf['content_border_red'].set_left()
    #     wbf['content_border_red'].set_right()
    #     wbf['content_border_red'].set_text_wrap()
    #
    #     wbf['content_border_bg'] = workbook.add_format(
    #         {'align': 'center', 'valign': 'vcenter', 'bold': 1, 'bg_color': '#E1E1E1'})
    #     wbf['content_border_bg'].set_top()
    #     wbf['content_border_bg'].set_bottom()
    #     wbf['content_border_bg'].set_left()
    #     wbf['content_border_bg'].set_right()
    #     wbf['content_border_bg'].set_text_wrap()
    #
    #     wbf['content_float_border'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00'})
    #     wbf['content_float_border'].set_top()
    #     wbf['content_float_border'].set_bottom()
    #     wbf['content_float_border'].set_left()
    #     wbf['content_float_border'].set_right()
    #
    #     wbf['content_int_border'] = workbook.add_format({'align': 'right', 'num_format': '#,##0'})
    #     wbf['content_int_border'].set_top()
    #     wbf['content_int_border'].set_bottom()
    #     wbf['content_int_border'].set_left()
    #     wbf['content_int_border'].set_right()
    #
    #     wbf['content_float_border_total'] = workbook.add_format(
    #         {'align': 'right', 'num_format': '#,##0.00', 'bold': 1, 'bg_color': '#E1E1E1'})
    #     wbf['content_float_border_total'].set_top()
    #     wbf['content_float_border_total'].set_bottom()
    #     wbf['content_float_border_total'].set_left()
    #     wbf['content_float_border_total'].set_right()
    #
    #     wbf['content_int_border_total'] = workbook.add_format(
    #         {'align': 'right', 'num_format': '#,##0', 'bold': 1, 'bg_color': '#E1E1E1'})
    #     wbf['content_int_border_total'].set_top()
    #     wbf['content_int_border_total'].set_bottom()
    #     wbf['content_int_border_total'].set_left()
    #     wbf['content_int_border_total'].set_right()
    #
    #     rowno = 1
    #     colno = 0
    #
    #     colno = 0
    #     column_width = 10
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Sl#', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 20
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Invoice No', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 15
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Invoice Date', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 15
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Due on', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 25
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Sales Person', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 50
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Partner Name', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 15
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Total Amount', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 15
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Due Amount', wbf['content_border_bg'])
    #
    #     colno += 1
    #     column_width = 15
    #     sheet.set_column(colno, colno, column_width)
    #     sheet.write(rowno - 1, colno, 'Paid', wbf['content_border_bg'])
    #
    #     objinvoiceln = self.env['account.move.line'].search([('move_id', 'in', invoiceids)], order='id')
    #
    #     for rec in objinvoiceln:
    #         colno = 0
    #         sheet.write(rowno, colno, rowno, wbf['content_border'])
    #         colno += 1
    #         sheet.write(rowno, colno, str(rec.name if rec.name else ""), wbf['content_border'])
    #
    #         colno += 1
    #         sheet.write(rowno, colno, str(rec.invoice_date.strftime('%d-%m-%Y')), wbf['content_border'])
    #         colno += 1
    #         sheet.write(rowno, colno, str(rec.invoice_payment_term_id.name if rec.invoice_payment_term_id.name else ""),
    #                     wbf['content_border'])
    #         colno += 1
    #         sheet.write(rowno, colno, str(rec.invoice_user_id.name if rec.invoice_user_id.name else ""),
    #                     wbf['content_border'])
    #         colno += 1
    #         sheet.write(rowno, colno, rec.partner_id.name if rec.partner_id.name else "", wbf['content_border'])
    #
    #         colno += 1
    #         sheet.write(rowno, colno, rec.amount_total_signed, wbf['content_float_border'])
    #         colno += 1
    #         sheet.write(rowno, colno, rec.amount_residual_signed, wbf['content_float_border'])
    #         colno += 1
    #         sheet.write(rowno, colno, ((rec.amount_total_signed) - (rec.amount_residual_signed)),
    #                     wbf['content_float_border'])
    #
    #         rowno += 1
    #     sheet.merge_range(rowno, 0, rowno, 5, "Total", wbf['content_border_bg'])
    #     colno = 6
    #     sheet.write(rowno, colno, "=sum(G2:G" + str(rowno) + ")", wbf['content_int_border_total'])
    #     colno = 7
    #     sheet.write(rowno, colno, "=sum(H2:H" + str(rowno) + ")", wbf['content_float_border_total'])
    #     colno = 8
    #     sheet.write(rowno, colno, "=sum(I2:I" + str(rowno) + ")", wbf['content_float_border_total'])
    #
    #     rowno += 1
    #
    #     workbook.close()
    #     out = base64.encodestring(fp.getvalue())
    #     self.write({'datas': out, 'datas_fname': filename})
    #     fp.close()
    #     filename += '%2Exlsx'
    #
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'target': 'new',
    #         'url': 'web/content/?model=' + self._name + '&id=' + str(
    #             self.id) + '&field=datas&download=true&filename=' + filename,
    #     }

