# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_kit_picking = fields.Boolean(string='Is Kit Picking', compute='_compute_is_kit_picking', store=True)
    kit_picking_line_ids = fields.One2many('stock.kit.picking.line', 'picking_id', string='Kit Picking Items')
    
    kit_product_move_count = fields.Integer(string='Kit Move Count', compute='_compute_kit_move_counts')
    bom_overhead_move_count = fields.Integer(string='BOM Overhead Move Count', compute='_compute_kit_move_counts')

    @api.depends('move_ids', 'sale_id')
    def _compute_is_kit_picking(self):
        for picking in self:
            is_kit = False
            if picking.sale_id:
                for line in picking.sale_id.order_line:
                    boms = self.env['mrp.bom'].search([
                        ('product_id', '=', line.product_id.id),
                        ('type', '=', 'phantom')
                    ], limit=1)
                    if not boms:
                        boms = self.env['mrp.bom'].search([
                            ('product_tmpl_id', '=', line.product_template_id.id),
                            ('type', '=', 'phantom')
                        ], limit=1)
                    if boms:
                        is_kit = True
                        break
            picking.is_kit_picking = is_kit

    @api.depends('sale_id', 'state')
    def _compute_kit_move_counts(self):
        for picking in self:
            if 'stock.valuation.layer' in self.env:
                layers = picking.move_ids.mapped('stock_valuation_layer_ids') if hasattr(picking.move_ids, 'stock_valuation_layer_ids') else self.env['stock.valuation.layer'].search([('stock_move_id', 'in', picking.move_ids.ids)])
                picking.kit_product_move_count = len(layers.mapped('account_move_id'))
            else:
                picking.kit_product_move_count = 0
            
            overhead_moves = self.env['account.move'].search([('stock_picking_overhead_id', '=', picking.id)])
            picking.bom_overhead_move_count = len(overhead_moves)

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for picking in self:
            if picking.is_kit_picking:
                picking._process_kit_overheads()
        return res
        
    def _process_kit_overheads(self):
        self.ensure_one()
        AccountMove = self.env['account.move']
        
        for move in self.move_ids:
            if move.state == 'done':
                boms = self.env['mrp.bom'].search([('product_id', '=', move.product_id.id), ('type', '=', 'phantom')], limit=1)
                if not boms:
                    boms = self.env['mrp.bom'].search([('product_tmpl_id', '=', move.product_id.product_tmpl_id.id), ('type', '=', 'phantom')], limit=1)
                
                if boms:
                    kit_line = self.kit_picking_line_ids.filtered(lambda l: l.product_id == move.product_id)
                    done_qty = move.quantity if hasattr(move, 'quantity') else move.product_uom_qty
                    if not kit_line:
                        self.env['stock.kit.picking.line'].create({
                            'picking_id': self.id,
                            'product_id': move.product_id.id,
                            'demand_qty': move.product_uom_qty,
                            'delivered_qty': done_qty,
                            'unit_price': move.product_id.list_price,
                        })
                    else:
                        kit_line.write({
                            'delivered_qty': done_qty,
                        })
                        
                    for ovh in boms.overhead_line_ids:
                        ovh_qty = ovh.quantity * done_qty
                        ovh_cost = ovh_qty * ovh.unit_cost
                        if ovh_cost > 0:
                            ovh_type = ovh.overhead_type_id or (ovh.product_id.product_tmpl_id.overhead_type_id if ovh.product_id else False)
                            if not ovh_type:
                                raise UserError(_("Overhead Type must be assigned for product %s to generate accounting entries.") % ovh.product_id.display_name)
                                
                            journal = ovh_type.journal_id
                            if not journal:
                                raise UserError(_("Accounting Journal is missing for Overhead Type: %s") % ovh_type.name)
                                
                            debit_account = ovh_type.expense_account_id or (ovh.product_id.property_account_expense_id if ovh.product_id else False)
                            if not debit_account:
                                raise UserError(_("Debit/Expense Account is missing for Overhead Type: %s") % ovh_type.name)
                                
                            credit_account = ovh_type.credit_account_id or (ovh.product_id.property_account_income_id if ovh.product_id else False)
                            if not credit_account:
                                raise UserError(_("Credit/Accrual Account is missing for Overhead Type: %s") % ovh_type.name)
                                
                            move_vals = {
                                'journal_id': journal.id,
                                'date': fields.Date.context_today(self),
                                'ref': _('Kit Overhead: %s - %s', self.name, ovh.product_id.display_name),
                                'stock_picking_overhead_id': self.id,
                                'line_ids': [
                                    (0, 0, {
                                        'name': _('Overhead Debit: %s', ovh.product_id.display_name),
                                        'account_id': debit_account.id,
                                        'debit': ovh_cost,
                                        'credit': 0.0,
                                    }),
                                    (0, 0, {
                                        'name': _('Overhead Credit: %s', ovh.product_id.display_name),
                                        'account_id': credit_account.id,
                                        'debit': 0.0,
                                        'credit': ovh_cost,
                                    }),
                                ]
                            }
                            new_move = AccountMove.create(move_vals)
                            new_move.action_post()

    def action_update_kit_qty(self):
        self.ensure_one()
        return {
            'name': _('Update Quantity Of Kit'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.kit.qty.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_picking_id': self.id},
        }

    def action_print_kit_delivery_slip(self):
        self.ensure_one()
        return self.env.ref('advance_mrp_costing_ucs.action_report_kit_delivery_slip').report_action(self)

    def action_view_kit_product_moves(self):
        self.ensure_one()
        layers = self.move_ids.mapped('stock_valuation_layer_ids') if hasattr(self.move_ids, 'stock_valuation_layer_ids') else self.env['stock.valuation.layer'].search([('stock_move_id', 'in', self.move_ids.ids)])
        return {
            'name': _('Kit Product Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', layers.mapped('account_move_id').ids)],
        }

    def action_view_bom_overhead_moves(self):
        self.ensure_one()
        return {
            'name': _('BOM Variable Overhead Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('stock_picking_overhead_id', '=', self.id)],
        }

class AccountMoveKitPicking(models.Model):
    _inherit = 'account.move'

    stock_picking_overhead_id = fields.Many2one('stock.picking', string='Kit Picking (Overhead)', ondelete='set null')


class StockKitPickingLine(models.Model):
    _name = 'stock.kit.picking.line'
    _description = 'Stock Kit Picking Component Details'

    picking_id = fields.Many2one('stock.picking', string='Stock Picking', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', string='Kit Product', required=True)
    demand_qty = fields.Float(string='Demand Quantity', default=1.0)
    delivered_qty = fields.Float(string='Delivered Quantity', default=0.0)
    unit_price = fields.Float(string='Unit Price', default=0.0)
    delivered_price = fields.Float(string='Delivered Price', compute='_compute_pricing', store=True)
    qty_deviation = fields.Float(string='Quantity Deviation', compute='_compute_pricing', store=True)
    price_deviation = fields.Float(string='Price Deviation', compute='_compute_pricing', store=True)

    @api.depends('demand_qty', 'delivered_qty', 'unit_price')
    def _compute_pricing(self):
        for line in self:
            line.delivered_price = line.delivered_qty * line.unit_price
            line.qty_deviation = line.delivered_qty - line.demand_qty
            line.price_deviation = line.delivered_price - (line.demand_qty * line.unit_price)
