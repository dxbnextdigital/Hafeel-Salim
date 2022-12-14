# See LICENSE file for full copyright and licensing details.


from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        partner = self.partner_id
        user_id = self.env['res.users'].search([
            ('partner_id', '=', partner.id)], limit=1)
        if user_id and not user_id.has_group('base.group_portal') or not \
                user_id:
            moveline_obj = self.env['account.move.line']
            movelines = moveline_obj.search(
                [('partner_id', '=', partner.id),
                 ('account_id.user_type_id.name', 'in',
                  ['Receivable', 'Payable'])]
            )
            # confirm_sale_order = self.search([('partner_id', '=', partner.id),
            #                                   ('state', '=', 'sale')])
            debit, credit = 0.0, 0.0
            amount_total = 0.0
            if partner.block_nonpayment:
                msg = 'Cannot processed due to non payment for due invoices.' \
                      '\nIf require to processed further please contact the administrator.'

                raise UserError(_('You can not confirm Sale '
                                  'Order. \n' + msg))
            else:
                if partner.over_credit:
                    return True
                else:

                    for status in self:
                        amount_total += status.amount_total
                    print(amount_total)
                    for line in movelines:
                        credit += line.credit
                        debit += line.debit
                    partner_credit_limit = (partner.credit_limit - debit) + credit
                    available_credit_limit = \
                        (partner_credit_limit - debit)
                    # if (amount_total - debit) > available_credit_limit:
                    #     if not partner.over_credit:
                    #         # msg = 'Your available credit limit' \
                    #         #       ' Amount = %s \nCheck "%s" Accounts or Credit ' \
                    #         #       'Limits.' % (partner.credit_limit,
                    #         #                    self.partner_id.name)
                    #
                    #         msg = 'The transaction amount is over and above the credit limit (AED %s).' \
                    #             '\nIf require to processed further please increase the credit limit. ' % format((partner.credit_limit), '.2f')
                    #
                    #         raise UserError(_('You can not confirm Sale '
                    #                           'Order. \n' + msg))
                    # partner.write(
                    #     {'credit_limit': credit - debit + self.amount_total})
                    tot = 0.00
                    partner_lmt = 0.00
                    is_unlimited = False
                    strdate = ''
                    for rec in self:
                        partner_lmt += rec.partner_id.credit_limit
                        is_unlimited = rec.partner_id.over_credit
                        objinv = self.env['account.move'].search(
                            [('partner_id', '=', rec.partner_id.id), ('move_type', '=', 'out_invoice'),
                             ('state', '=', 'posted'),
                             ('amount_residual', '>', 0.0)])
                        for recinv in objinv:
                            tot += recinv.amount_residual
                        print(((partner_lmt - tot) - rec.amount_total))
                        if ((partner_lmt - tot) - rec.amount_total) < 0:
                            msg = 'The transaction amount is over and above the credit limit (AED %s).' \
                                  '\nIf require to processed further please increase the credit limit. ' % format(
                                (partner_lmt), '.2f')

                            raise UserError(_('You can not confirm Sale '
                                              'Order. \n' + msg))
            return True

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res

    @api.constrains('amount_total')
    def check_amount(self):
        for order in self:
            order.check_limit()
