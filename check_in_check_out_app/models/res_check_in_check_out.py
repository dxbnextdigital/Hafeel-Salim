from odoo import fields, models, api,_


class ResCheckIn(models.Model):
    _name = 'res.check'
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one("res.partner" , required=True)
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    planed_date = fields.Date(string="Planed Date" , required=True)
    note = fields.Text(string="Note")
    state =  fields.Selection([("draft", "Draft"), ("checkin", "Check In"),("checkout","Check Out"),("cancel","Cancel")], string="State", default="draft")
    time_status = fields.Selection([('today','Today'),('overdue','Overdue'),('upcoming','Upcoming'),('completed','Completed')],compute="check_today_upcoming_overdue",store=True)
    user_id = fields.Many2one('res.users', string='Assigned', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    @api.depends('planed_date','check_out','state')
    def check_today_upcoming_overdue(self):
        today = fields.Date.today()
        for rec in self:
            if rec.state in ['draft','checkin']:
                if rec.planed_date:
                    if rec.planed_date == today:
                        rec.time_status = 'today'
                    if rec.planed_date < today:
                        rec.time_status ='overdue'
                    if rec.planed_date > today:
                        rec.time_status = 'upcoming'
            else:
                rec.time_status = 'completed'

    def action_check_in(self):
        self.check_in = fields.datetime.now()
        self.state='checkin'

    def action_check_out(self):
        self.state='checkout'
        self.check_out = fields.datetime.now()


    def action_cancel(self):
        self.state='cancel'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('res.check') or _('New')
        res = super(ResCheckIn, self).create(vals)
        return res
