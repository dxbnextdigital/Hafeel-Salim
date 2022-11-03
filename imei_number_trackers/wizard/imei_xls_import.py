import io
import xlrd
import babel
import logging
import tempfile
import binascii
from io import StringIO
from datetime import date, datetime, time
from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError, ValidationError
_logger = logging.getLogger(__name__)

import  json
try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
from odoo.tools import date_utils


class ImportEmployee(models.TransientModel):
	_name = 'imei.xls.import'
	_description = 'Import IMEI'
	sale_order_id = fields.Many2one('sale.order')
	file_type = fields.Selection([('XLS', 'XLS File')],string='File Type', default='XLS')
	file = fields.Binary(string="Upload File")


	def export_export_product(self):
		data = {
			'ids': self.id,
			'model': self._name,
			'sale_order_id': self.sale_order_id.id,

		}
		return {
			'type': 'ir.actions.report',
			'data': {'model': 'imei.xls.import',
					 'options': json.dumps(data, default=date_utils.json_default),
					 'output_format': 'xlsx',
					 'report_name': self.sale_order_id.name+"_IMEI_EXPORT",
					 },
			'report_type': 'xlsx'
		}

	def get_product(self, name):
		product = self.env['product.product'].search([('name', '=', name)],limit=1)
		if product:
			return product
		else:
			raise UserError(_('"%s" Product is not found in system !') % name)

	def remove_decimal(self,value):
		if '.' in value:
			value = value.split(".")[0]
		return value

	def create_employee(self, values):
		print('create_employee')
		imei_number = self.env['imei.number']
		product_id = self.get_product(values.get('Product'))
		print("yes")
		print(self.remove_decimal(values.get('IMEI')))
		vals = {
			'product_id': product_id.id,
			'name': self.remove_decimal(values.get('IMEI')),
			'sale_order': self.sale_order_id.id

		}

		if values.get('name') == '':
			raise UserError(_('IMEI Name is Required !'))
		if values.get('product_id') == '':
			raise UserError(_('Product Field can not be Empty !'))

		res = imei_number.create(vals)
		return ;

	def import_imei_numbers(self):
		if not self.file:
			raise ValidationError(_("Please Upload File to Import IMEI !"))

		if self.file_type == 'CSV':
			line = keys = ['Product', 'IMEI']
			try:
				csv_data = base64.b64decode(self.file)
				data_file = io.StringIO(csv_data.decode("utf-8"))
				data_file.seek(0)
				file_reader = []
				csv_reader = csv.reader(data_file, delimiter=',')
				file_reader.extend(csv_reader)
			except Exception:
				raise ValidationError(_("Please Select Valid File Format !"))

			values = {}
			for i in range(len(file_reader)):
				field = list(map(str, file_reader[i]))
				values = dict(zip(keys, field))
				if values:
					if i == 0:
						continue
					else:

						res = self.create_employee(values)
		else:
			try:
				file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
				file.write(binascii.a2b_base64(self.file))
				file.seek(0)
				values = {}
				workbook = xlrd.open_workbook(file.name)
				sheet = workbook.sheet_by_index(0)
			except Exception:
				raise ValidationError(_("Please Select Valid File Format !"))
			sale_list = []
			for row_no in range(sheet.nrows):
				val = {}
				print(row_no)
				if row_no <= 0:
					fields = list(map(lambda row: row.value.encode('utf-8'), sheet.row(row_no)))
				else:
					line = list(
						map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
							sheet.row(row_no)))
					values = {'Product': line[0], 'IMEI': line[1]}
					sale_list.append(values)


			# print(sale_list)
			self.sale_order_id.pre_xls_entry_before(sale_list)
			#
			for rec in sale_list:
			# 	print(rec)
				res = self.create_employee(rec)
			self.sale_order_id.check_imei_number_correct()


	def get_xlsx_report(self, data, response):
		print('data',data)
		print('response',response)
		output = io.BytesIO()
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		worksheet = workbook.add_worksheet()

		my_dict = {'Product': [],
				   'IMEI': [],
				 }

		col_num = 0
		for rec in self.env['sale.order.line'].search([('order_id','=',data['sale_order_id']),('product_id.is_imei_required','=',True)]):
			for qty in range(int(rec.product_uom_qty)):
				my_dict['Product'].append(rec.product_id.name)
				my_dict['IMEI'].append(0)
		print(my_dict)
		for key, value in my_dict.items():
			worksheet.write(0, col_num, key)
			worksheet.write_column(1, col_num, value)
			col_num += 1

		workbook.close()
		output.seek(0)
		response.stream.write(output.read())
		output.close()



