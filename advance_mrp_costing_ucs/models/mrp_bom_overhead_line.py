# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpBomOverheadLine(models.Model):
    _name = 'mrp.bom.overhead.line'
    _description = 'BOM Variable & Fixed Overhead Line'

    bom_id = fields.Many2one('mrp.bom', string='Bill of Materials', ondelete='cascade', required=True)
    product_id = fields.Many2one(
        'product.product', 
        string='Overhead Item (Service Product)', 
        domain="[('type', '=', 'service')]",
        required=True
    )
    overhead_type_id = fields.Many2one(
        'mrp.overhead.type', 
        string='Overhead Type', 
        compute='_compute_overhead_type',
        store=True,
        readonly=False
    )
    cost_category = fields.Selection([
        ('fixed', 'Fixed Cost'),
        ('per_unit', 'Per Unit Produced'),
        ('percentage_material', '% of Material Cost')
    ], string='Calculation Basis', default='per_unit', required=True)
    
    quantity = fields.Float(string='Quantity / Rate %', default=1.0)
    unit_cost = fields.Float(string='Unit Cost', default=0.0)
    total_cost = fields.Float(string='Total Overhead Cost', compute='_compute_total_cost', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='bom_id.company_id.currency_id')

    @api.depends('product_id')
    def _compute_overhead_type(self):
        for line in self:
            if line.product_id and line.product_id.product_tmpl_id.overhead_type_id:
                line.overhead_type_id = line.product_id.product_tmpl_id.overhead_type_id
            elif not line.overhead_type_id:
                line.overhead_type_id = False

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_cost = self.product_id.standard_price
            if self.product_id.product_tmpl_id.overhead_type_id:
                self.overhead_type_id = self.product_id.product_tmpl_id.overhead_type_id

    @api.depends('cost_category', 'quantity', 'unit_cost', 'bom_id.total_material_cost', 'bom_id.product_qty')
    def _compute_total_cost(self):
        for line in self:
            if line.cost_category == 'fixed':
                line.total_cost = line.quantity * line.unit_cost
            elif line.cost_category == 'per_unit':
                line.total_cost = line.quantity * line.unit_cost * (line.bom_id.product_qty or 1.0)
            elif line.cost_category == 'percentage_material':
                material_cost = line.bom_id.total_material_cost if line.bom_id else 0.0
                line.total_cost = (line.quantity / 100.0) * material_cost
            else:
                line.total_cost = 0.0
