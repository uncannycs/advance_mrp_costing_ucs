# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockKitQtyWizard(models.TransientModel):
    _name = 'stock.kit.qty.wizard'
    _description = 'Update Quantity Of Kit Product Wizard'

    picking_id = fields.Many2one('stock.picking', string='Stock Picking', required=True)
    kit_qty = fields.Float(string='New Kit Quantity', default=1.0, required=True)

    def action_update(self):
        self.ensure_one()
        if self.kit_qty <= 0:
            raise UserError(_('Quantity must be greater than zero.'))
            
        picking = self.picking_id
        if picking and picking.sale_id:
            for line in picking.sale_id.order_line:
                # Update sale order line quantity for kit items
                line.product_uom_qty = self.kit_qty
        
        # Populate or update stock.kit.picking.line records
        for move in picking.move_ids:
            kit_line = picking.kit_picking_line_ids.filtered(lambda l: l.product_id == move.product_id)
            if kit_line:
                kit_line.write({
                    'demand_qty': self.kit_qty,
                    'delivered_qty': self.kit_qty,
                })
            else:
                self.env['stock.kit.picking.line'].create({
                    'picking_id': picking.id,
                    'product_id': move.product_id.id,
                    'demand_qty': self.kit_qty,
                    'delivered_qty': self.kit_qty,
                    'unit_price': move.product_id.list_price,
                })
                
        return {'type': 'ir.actions.act_window_close'}
