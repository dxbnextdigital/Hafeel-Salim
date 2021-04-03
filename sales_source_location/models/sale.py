# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    custom_source_location_id = fields.Many2one(
        'stock.location',
        'Source Location',
        required=True,
    )
    custom_source_id = fields.Many2one(
        'custom.source.location',
        'Source',
        default=lambda self: self.env.user.custom_source_id.id
    )
    user_location = fields.Integer(default=lambda self: self.env.user.custom_source_id.id)

    credit_limit_msg = fields.Text(compute='_current_creditlimit')

    @api.depends('partner_id')
    def _current_creditlimit(self):
        tot=0.00
        partner_lmt =0.00
        is_unlimited =False
        strdate =''
        for rec in self:
            partner_lmt+=rec.partner_id.credit_limit
            is_unlimited =rec.partner_id.over_credit
            objinv = self.env['account.move'].search([('partner_id', '=', rec.partner_id.id), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), ('amount_residual', '>', 0.0)])
            for recinv in objinv:
                tot += recinv.amount_residual

            # if is_unlimited:
            #     rec.credit_limit_msg = 'Amount due as on date AED %s. |  Credit Limit is AED %s. |  Available Limit is AED %s.' % format(
            #         tot, '.2f')
            # else:
            rec.credit_limit_msg = 'Amount due as on date AED %s. |  Credit Limit is AED %s. |  Available Limit is AED %s. | Allow Over Credit : %s' % (
            format(
                tot, '.2f'), format(partner_lmt, '.2f'), format(partner_lmt - tot, '.2f'), is_unlimited)

    @api.onchange('custom_source_id')
    def _onchange_custom_source_id(self):
        self.analytic_account_id = self.custom_source_id.analytic_account_id.id
        self.custom_source_location_id = self.custom_source_id.stock_location_id.id

    def action_confirm_deliver(self):

        for rec in self:
            lineno =1
            for recln in rec.order_line:
                if recln.product_uom_qty>recln.my_stock:
                 raise UserError('Trying to Sell more product than the available stock at line no : ' + str(lineno))
                lineno+=1
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        for pick in self.picking_ids:
            if pick.state not in ('done','cancel'):
                result =pick.button_validate()
                resin=self._create_invoice_fromso()
                #raise UserError('ok')

        return result


    def _create_invoice_fromso(self):

        for so in self:
            move_line_vals = []

            for line in so.order_line:
                create_vals = (0, 0, {
                    'date': datetime.now(),
                    'name': line.product_id.name,
                    # 'ref': so.client_order_ref,
                    # 'payment_reference': so.name,
                    'discount': line.discount,
                    'parent_state': 'draft',
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'product_uom_id': line.product_uom.id,
                    'product_id': line.product_id.id,
                    'sale_line_ids': [(6, 0, [line.id])],
                    'analytic_account_id': so.analytic_account_id.id or False,
                    'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    'tax_ids': [(6, 0, line.tax_id.ids)],

                })
                # totalamt += line.price_total
                move_line_vals.append(create_vals)

            move_vals = {'date': datetime.now(),
                         'partner_id': so.partner_id.id,
                         'invoice_origin':  str(so.name),
                         'invoice_date': datetime.now(),
                         'narration': so.note,
                         #'journal_id': 1,
                         'team_id': so.team_id.id,
                         'invoice_user_id': so.user_id.id,
                         'invoice_payment_term_id': so.payment_term_id.id,
                         'ref': so.client_order_ref,
                         'payment_reference': so.name,
                         'name': '/',
                         'state': 'draft',
                         'move_type': 'out_invoice',
                         'invoice_line_ids': move_line_vals,
                         'campaign_id': so.campaign_id.id,
                         'medium_id': so.medium_id.id,
                         'source_id': so.source_id.id,
                         'fiscal_position_id': (
                                     so.fiscal_position_id or so.fiscal_position_id.get_fiscal_position(
                                 so.partner_id.id)).id,
                         'partner_shipping_id': so.partner_shipping_id.id,
                         'currency_id': so.pricelist_id.currency_id.id,
                         }
            objacmove = self.env['account.move'].create(move_vals)
            objacmove.post()



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_client_order_ref = fields.Char(
        string='Customer Reference',
        related='order_id.client_order_ref',
        store=True,
    )
    my_stock = fields.Float('AVL QTY', compute='_avlqty', store=True)
 #   brand = fields.Many2one('mis.product.brand', string='Brand', related='product_id.brand')

    #
    # @api.depends('product_id','product_uom_qty')
    # def _checkavailablity(self):
    #     raise UserError('Trying to Sell more product than the available stock')
    #     for rec in self:
    #         if rec.product_uom_qty>rec.my_stock:
    #             raise UserError('Trying to Sell more product than the available stock')

    @api.depends('product_id','product_uom_qty','order_id.custom_source_location_id')
    def _avlqty(self):
        for rec in self:
            if rec.product_id and rec.order_id.custom_source_location_id:
                stquant = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id), ('location_id', '=', rec.order_id.custom_source_location_id.id)])
                avlqty =0.0
                for recst in stquant:
                    avlqty+=recst.quantity
                rec.my_stock=avlqty


    def _prepare_invoice_custom(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
#        self.ensure_one()
        # ensure a correct context for the _get_default_journal method and company-dependent fields
        if len(self.mapped('order_id').mapped('partner_id').ids) > 1:
            raise UserError(_("To create invoice Customer must be same of selected sale order lines"))
        so_order_id = self.mapped('order_id')[0]
        so_order_id = so_order_id.with_context(default_company_id=so_order_id.company_id.id, force_company=so_order_id.company_id.id)
        journal = so_order_id.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (so_order_id.company_id.name, so_order_id.company_id.id))

        invoice_vals = {
#            'ref': self.client_order_ref or '',
            'type': 'out_invoice',
#            'narration': self.note,
#            'currency_id': self.pricelist_id.currency_id.id,
#            'campaign_id': self.campaign_id.id,
#            'medium_id': self.medium_id.id,
#            'source_id': self.source_id.id,
            'invoice_user_id': so_order_id.user_id and so_order_id.user_id.id,
#            'team_id': self.team_id.id,
            'partner_id': so_order_id.partner_invoice_id.id,
            'partner_shipping_id': so_order_id.partner_shipping_id.id,
            'invoice_partner_bank_id': so_order_id.company_id.partner_id.bank_ids[:1].id,
            'fiscal_position_id': so_order_id.fiscal_position_id.id or so_order_id.partner_invoice_id.property_account_position_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': so_order_id.name,
#            'invoice_payment_term_id': self.payment_term_id.id,
#            'invoice_payment_ref': self.reference,
#            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': so_order_id.company_id.id,
        }
        return invoice_vals

    def _prepare_invoice_line_custom(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.display_type:
            res['account_id'] = False
        return res


    def create_inv_custom(self):
        invoice_vals = self._prepare_invoice_custom()
        for line in self:
            if line.qty_to_invoice > 0:
                invoice_vals['invoice_line_ids'].append((0, 0, line._prepare_invoice_line_custom()))
        
        if not invoice_vals['invoice_line_ids']:
            raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
        moves = self.env['account.move'].sudo().with_context(default_type='out_invoice').create(invoice_vals)
        return moves

class MisSaleReport(models.Model):
    _inherit = "sale.report"

    brand = fields.Many2one('mis.product.brand', string="Brand")



