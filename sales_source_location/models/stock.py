# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _write(self, vals):
        res = super(StockPicking, self)._write(vals)
        if vals.get('sale_id'):
            for rec in self:
                rec.location_id = rec.sale_id.custom_source_location_id.id
        return res


class StockMoveLineCustom(models.Model):
    _inherit = 'stock.move.line'

    loc_stock = fields.Float('AVL QTY', compute='_avlqty', store=True)

    @api.depends('product_id', 'picking_id.location_id')
    def _avlqty(self):
        for rec in self:
            if rec.product_id and rec.picking_id.location_id:
                stquant = self.env['stock.quant'].search(
                    [('product_id', '=', rec.product_id.id), ('location_id', '=', rec.picking_id.location_id.id)])
                avlqty = 0.0
                for recst in stquant:
                    avlqty += recst.quantity
                rec.loc_stock = avlqty

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_qty_onhand = fields.Float(
        string='Onhand Quantity',
    )



    @api.model
    def create(self, vals):
        rec = super(StockMove, self).create(vals)
        if vals.get('product_id'):
            rec.product_qty_onhand = rec.product_id.qty_available
        return rec
    
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        if vals.get('product_id'):
            for rec in self:
                rec.product_qty_onhand = rec.product_id.qty_available
        return res
