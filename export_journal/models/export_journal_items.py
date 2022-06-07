from odoo import models, fields, api


class ExportJournalItems(models.Model):
    _name = 'export.journal.item'
    _description = 'Action Window2'
    from_journal = fields.Many2one('account.account',string="from")
    journal_id = fields.Many2one('account.account',string="to")
    change_account_id = fields.Many2one('account.account',string="change account")
    change_account_type = fields.Many2one('account.account.type',string="change type")
    def xlsx_export_journal(self):
        sql ="UPDATE account_move_line SET account_id = '"+str(self.journal_id.id)+"' where account_id= '"+str(self.from_journal.id)+"'"
        print(sql)
        self.env.cr.execute(sql)
    def change_account_type_fun(self):
        sql = "UPDATE account_account SET user_type_id = '" + str(self.change_account_type.id) + "' where id= '" + str(
            self.change_account_id.id) + "'"
        print(sql)
        self.env.cr.execute(sql)
