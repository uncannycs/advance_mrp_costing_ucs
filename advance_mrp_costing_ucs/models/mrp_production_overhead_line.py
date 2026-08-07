# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpProductionOverheadLine(models.Model):
    _name = 'mrp.production.overhead.line'
    _description = 'Manufacturing Order Extra Overhead Line'

    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', ondelete='cascade', required=True)
    product_id = fields.Many2one(
        'product.product', 
        string='Overhead Item', 
        domain="[('type', '=', 'service')]",
        required=True
    )
    overhead_type_id = fields.Many2one('mrp.overhead.type', string='Overhead Type')
    cost_category = fields.Selection([
        ('fixed', 'Fixed Cost'),
        ('per_unit', 'Per Unit Produced'),
        ('percentage_material', '% of Material Cost')
    ], string='Calculation Basis', default='per_unit', required=True)
    
    planned_qty = fields.Float(string='Planned Qty / %', default=1.0)
    actual_qty = fields.Float(string='Actual Qty / %', default=1.0)
    unit_cost = fields.Float(string='Unit Cost Rate', default=0.0)
    
    planned_cost = fields.Float(string='Planned Cost', compute='_compute_costs', store=True)
    actual_cost = fields.Float(string='Actual Cost', compute='_compute_costs', store=True)
    cost_deviation = fields.Float(string='Cost Variance', compute='_compute_costs', store=True)
    
    move_id = fields.Many2one('account.move', string='Overhead Journal Entry', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_cost = self.product_id.standard_price
            if self.product_id.product_tmpl_id.overhead_type_id:
                self.overhead_type_id = self.product_id.product_tmpl_id.overhead_type_id

    @api.depends('cost_category', 'planned_qty', 'actual_qty', 'unit_cost', 'production_id.product_qty', 'production_id.qty_producing')
    def _compute_costs(self):
        for line in self:
            planned_prod_qty = line.production_id.product_qty or 1.0
            actual_prod_qty = line.production_id.qty_producing or planned_prod_qty
            
            if line.cost_category == 'fixed':
                line.planned_cost = line.planned_qty * line.unit_cost
                line.actual_cost = line.actual_qty * line.unit_cost
            elif line.cost_category == 'per_unit':
                line.planned_cost = line.planned_qty * line.unit_cost * planned_prod_qty
                line.actual_cost = line.actual_qty * line.unit_cost * actual_prod_qty
            elif line.cost_category == 'percentage_material':
                planned_mat = line.production_id.total_planned_material_cost if line.production_id else 0.0
                actual_mat = line.production_id.total_actual_material_cost if line.production_id else 0.0
                line.planned_cost = (line.planned_qty / 100.0) * planned_mat
                line.actual_cost = (line.actual_qty / 100.0) * actual_mat
            else:
                line.planned_cost = 0.0
                line.actual_cost = 0.0
            
            line.cost_deviation = line.actual_cost - line.planned_cost
