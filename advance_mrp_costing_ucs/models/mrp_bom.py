# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    overhead_line_ids = fields.One2many('mrp.bom.overhead.line', 'bom_id', string='Variable Overhead Items', copy=True)
    
    total_material_cost = fields.Float(string='Total Material Cost', compute='_compute_bom_costs', store=True)
    total_overhead_cost = fields.Float(string='Total Overhead Cost', compute='_compute_bom_costs', store=True)
    total_bom_cost = fields.Float(string='Total BOM Cost', compute='_compute_bom_costs', store=True)
    unit_bom_cost = fields.Float(string='Unit Production Cost', compute='_compute_bom_costs', store=True)
    overhead_line_count = fields.Integer(string='Overhead Line Count', compute='_compute_bom_costs')

    @api.depends('bom_line_ids', 'bom_line_ids.product_id', 'bom_line_ids.product_qty', 'overhead_line_ids', 'overhead_line_ids.total_cost', 'product_qty')
    def _compute_bom_costs(self):
        for bom in self:
            mat_cost = 0.0
            for line in bom.bom_line_ids:
                unit_price = line.product_id.standard_price if line.product_id else 0.0
                mat_cost += line.product_qty * unit_price
            
            ovh_cost = sum(bom.overhead_line_ids.mapped('total_cost'))
            
            bom.total_material_cost = mat_cost
            bom.total_overhead_cost = ovh_cost
            bom.total_bom_cost = mat_cost + ovh_cost
            bom.unit_bom_cost = (mat_cost + ovh_cost) / (bom.product_qty or 1.0)
            bom.overhead_line_count = len(bom.overhead_line_ids)

    def action_view_overhead_details(self):
        self.ensure_one()
        return {
            'name': 'BOM Overhead Details',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.bom.overhead.line',
            'view_mode': 'list,pivot,graph',
            'domain': [('bom_id', '=', self.id)],
            'context': {'default_bom_id': self.id},
        }
