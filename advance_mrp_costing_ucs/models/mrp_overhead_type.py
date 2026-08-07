# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpOverheadType(models.Model):
    _name = 'mrp.overhead.type'
    _description = 'MRP Overhead Cost Type'
    _order = 'name'

    name = fields.Char(string='Overhead Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    
    expense_account_id = fields.Many2one('account.account', string='Debit/Expense Account', help='Account debited when overhead cost is recognized')
    credit_account_id = fields.Many2one('account.account', string='Credit/Accrual Account', help='Account credited when overhead cost is recognized')
    journal_id = fields.Many2one('account.journal', string='Accounting Journal', help='Journal used to post extra cost journal entries')
    
    product_ids = fields.One2many('product.template', 'overhead_type_id', string='Overhead Items')
    product_count = fields.Integer(string='Product Count', compute='_compute_counts')
    bom_count = fields.Integer(string='BOM Count', compute='_compute_counts')
    mo_count = fields.Integer(string='MO Count', compute='_compute_counts')

    @api.depends('product_ids')
    def _compute_counts(self):
        for rec in self:
            rec.product_count = len(rec.product_ids)
            
            # Count BOMs containing lines with this overhead type
            bom_lines = self.env['mrp.bom.overhead.line'].search([('overhead_type_id', '=', rec.id)])
            rec.bom_count = len(bom_lines.mapped('bom_id'))
            
            # Count MOs containing lines with this overhead type
            mo_lines = self.env['mrp.production.overhead.line'].search([('overhead_type_id', '=', rec.id)])
            rec.mo_count = len(mo_lines.mapped('production_id'))

    def action_view_products(self):
        self.ensure_one()
        return {
            'name': 'Overhead Products',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('overhead_type_id', '=', self.id)],
            'context': {'default_type': 'service', 'default_overhead_type_id': self.id},
        }

    def action_view_boms(self):
        self.ensure_one()
        bom_lines = self.env['mrp.bom.overhead.line'].search([('overhead_type_id', '=', self.id)])
        bom_ids = bom_lines.mapped('bom_id').ids
        return {
            'name': 'Bills of Materials',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.bom',
            'view_mode': 'list,form',
            'domain': [('id', 'in', bom_ids)],
        }

    def action_view_mos(self):
        self.ensure_one()
        mo_lines = self.env['mrp.production.overhead.line'].search([('overhead_type_id', '=', self.id)])
        mo_ids = mo_lines.mapped('production_id').ids
        return {
            'name': 'Manufacturing Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'list,form',
            'domain': [('id', 'in', mo_ids)],
        }
