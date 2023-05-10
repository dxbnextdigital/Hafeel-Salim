from odoo import fields, models, api,_
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
import xlsxwriter

class test(models.Model):
    _name= 'test.imei.one'

    def get_inform_missing(self):
        workbook = xlsxwriter.Workbook('/home/neeraj/Desktop/demo.xlsx')
        worksheet = workbook.add_worksheet()

        product_sql ='select name,product_id,invoice_date from imei_number where sale_order is null'
        self.env.cr.execute(product_sql)
        product_sql  = self.env.cr.dictfetchall()
        row = 0
        col = 0
        for rec in product_sql:
            sql = '''
            
                        SELECT count(move_name),move_name,product_id
                        FROM account_move_line
                        INNER JOIN account_move
                        ON account_move.id = account_move_line.move_id and account_move.invoice_date = '''+"'"+str(rec['invoice_date'])+"'"+''' and  product_id='''+str(rec['product_id'])+"   group by product_id,move_name "


            print(sql)




            self.env.cr.execute(sql)
            product = self.env.cr.dictfetchall()
            row = row+1
            worksheet.write(row, col, rec['name'])

            for pro in product:
                row = row +1
                worksheet.write(row , col, pro['count'])
                col = col+1
                worksheet.write(row , col, pro['move_name'])
                col = col+1
                worksheet.write(row , col, pro['product_id'])
                col = 0


        workbook.close()