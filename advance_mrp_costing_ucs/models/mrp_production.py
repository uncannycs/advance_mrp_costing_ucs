# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    overhead_line_ids = fields.One2many('mrp.production.overhead.line', 'production_id', string='Variable Overhead Items', copy=True)
    
    total_planned_material_cost = fields.Float(string='Planned Material Cost', compute='_compute_production_costs', store=True)
    total_actual_material_cost = fields.Float(string='Actual Material Cost', compute='_compute_production_costs', store=True)
    
    total_planned_overhead_cost = fields.Float(string='Planned Overhead Cost', compute='_compute_production_costs', store=True)
    total_actual_overhead_cost = fields.Float(string='Actual Overhead Cost', compute='_compute_production_costs', store=True)
    
    total_planned_production_cost = fields.Float(string='Planned Total Cost', compute='_compute_production_costs', store=True)
    total_actual_production_cost = fields.Float(string='Actual Total Cost', compute='_compute_production_costs', store=True)
    
    total_cost_variance = fields.Float(string='Total Cost Variance', compute='_compute_production_costs', store=True)
    
    overhead_move_ids = fields.One2many('account.move', 'mrp_production_overhead_id', string='Overhead Journal Entries')
    overhead_move_count = fields.Integer(string='Overhead Entry Count', compute='_compute_move_counts')
    main_product_move_count = fields.Integer(string='Main Product Entry Count', compute='_compute_move_counts')

    @api.depends('move_raw_ids', 'move_raw_ids.quantity', 'move_raw_ids.product_id', 'overhead_line_ids', 'overhead_line_ids.planned_cost', 'overhead_line_ids.actual_cost', 'product_qty', 'qty_producing')
    def _compute_production_costs(self):
        for mo in self:
            planned_mat = 0.0
            actual_mat = 0.0
            for move in mo.move_raw_ids:
                price = move.product_id.standard_price if move.product_id else 0.0
                planned_mat += move.product_uom_qty * price
                actual_mat += move.quantity * price
            
            planned_ovh = sum(mo.overhead_line_ids.mapped('planned_cost'))
            actual_ovh = sum(mo.overhead_line_ids.mapped('actual_cost'))
            
            mo.total_planned_material_cost = planned_mat
            mo.total_actual_material_cost = actual_mat
            mo.total_planned_overhead_cost = planned_ovh
            mo.total_actual_overhead_cost = actual_ovh
            
            mo.total_planned_production_cost = planned_mat + planned_ovh
            mo.total_actual_production_cost = actual_mat + actual_ovh
            mo.total_cost_variance = (actual_mat + actual_ovh) - (planned_mat + planned_ovh)

    @api.depends('overhead_move_ids', 'move_finished_ids', 'overhead_line_ids.move_id')
    def _compute_move_counts(self):
        for mo in self:
            mo.overhead_move_count = len(mo.overhead_move_ids)
            if 'stock.valuation.layer' in self.env:
                layers = mo.move_finished_ids.mapped('stock_valuation_layer_ids') if hasattr(mo.move_finished_ids, 'stock_valuation_layer_ids') else self.env['stock.valuation.layer'].search([('stock_move_id', 'in', mo.move_finished_ids.ids)])
                mo.main_product_move_count = len(layers.mapped('account_move_id'))
            else:
                mo.main_product_move_count = 0

    @api.onchange('bom_id')
    def _onchange_bom_id_overhead(self):
        if self.bom_id:
            overhead_lines = []
            for line in self.bom_id.overhead_line_ids:
                overhead_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'overhead_type_id': line.overhead_type_id.id if line.overhead_type_id else False,
                    'cost_category': line.cost_category,
                    'planned_qty': line.quantity,
                    'actual_qty': line.quantity,
                    'unit_cost': line.unit_cost,
                }))
            self.overhead_line_ids = [(5, 0, 0)] + overhead_lines

    @api.model_create_multi
    def create(self, vals_list):
        records = super(MrpProduction, self).create(vals_list)
        for rec in records:
            if rec.bom_id and not rec.overhead_line_ids:
                rec._onchange_bom_id_overhead()
        return records

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for mo in self:
            if not mo.overhead_line_ids and mo.bom_id and mo.bom_id.overhead_line_ids:
                for line in mo.bom_id.overhead_line_ids:
                    self.env['mrp.production.overhead.line'].create({
                        'production_id': mo.id,
                        'product_id': line.product_id.id if line.product_id else False,
                        'overhead_type_id': line.overhead_type_id.id if line.overhead_type_id else False,
                        'cost_category': line.cost_category,
                        'planned_qty': line.quantity,
                        'actual_qty': line.quantity or 1.0,
                        'unit_cost': line.unit_cost,
                    })
            mo._create_overhead_accounting_entries()
            mo._compute_move_counts()
        return res

    def action_generate_overhead_entries(self):
        for mo in self:
            if not mo.overhead_line_ids:
                bom_lines = mo.bom_id.overhead_line_ids if (mo.bom_id and mo.bom_id.overhead_line_ids) else False
                if bom_lines:
                    for line in bom_lines:
                        self.env['mrp.production.overhead.line'].create({
                            'production_id': mo.id,
                            'product_id': line.product_id.id if line.product_id else False,
                            'overhead_type_id': line.overhead_type_id.id if line.overhead_type_id else False,
                            'cost_category': line.cost_category,
                            'planned_qty': line.quantity,
                            'actual_qty': line.quantity or 1.0,
                            'unit_cost': line.unit_cost,
                        })
                else:
                    ovh_type = self.env['mrp.overhead.type'].search([], limit=1)
                    if not ovh_type:
                        raise UserError(_('Please configure at least one Overhead Type.'))
                    service_prod = (ovh_type.product_ids[0] if ovh_type and ovh_type.product_ids else False)
                    if not service_prod:
                        service_prod = self.env['product.product'].search([('type', '=', 'service')], limit=1)
                    if not service_prod:
                        raise UserError(_('Please configure at least one Service Product for Overhead.'))
                    self.env['mrp.production.overhead.line'].create({
                        'production_id': mo.id,
                        'product_id': service_prod.id,
                        'overhead_type_id': ovh_type.id,
                        'cost_category': 'labor',
                        'planned_qty': 1.0,
                        'actual_qty': 1.0,
                        'unit_cost': service_prod.standard_price,
                    })
            mo._create_overhead_accounting_entries()
            mo._compute_move_counts()
            mo._compute_production_costs()
        return True

    def _create_overhead_accounting_entries(self):
        self.ensure_one()
        AccountMove = self.env['account.move']
        for line in self.overhead_line_ids:
            actual_cost = line.actual_cost or (line.actual_qty * line.unit_cost)
            if not line.actual_cost and actual_cost:
                line.actual_cost = actual_cost
            if actual_cost > 0 and not line.move_id:
                ovh_type = line.overhead_type_id or (line.product_id.product_tmpl_id.overhead_type_id if line.product_id else False)
                if not ovh_type and line.product_id:
                    ovh_type = self.env['mrp.overhead.type'].search([('product_ids', 'in', line.product_id.product_tmpl_id.id)], limit=1)
                
                # Auto-link fallback if they accidentally created a duplicate product or forgot to link it
                if not ovh_type:
                    ovh_type = self.env['mrp.overhead.type'].search([], limit=1)
                    if ovh_type and line.product_id:
                        line.product_id.product_tmpl_id.overhead_type_id = ovh_type.id
                        line.overhead_type_id = ovh_type.id
                
                if not ovh_type:
                    raise UserError(_("Please create at least one Overhead Type in Configuration before generating entries."))
                
                journal = ovh_type.journal_id
                if not journal:
                    raise UserError(_("Accounting Journal is missing for Overhead Type: %s") % ovh_type.name)
                    
                debit_account = ovh_type.expense_account_id or (line.product_id.property_account_expense_id if line.product_id else False)
                if not debit_account:
                    raise UserError(_("Debit/Expense Account is missing for Overhead Type: %s") % ovh_type.name)
                    
                credit_account = ovh_type.credit_account_id or (line.product_id.property_account_income_id if line.product_id else False)
                if not credit_account:
                    raise UserError(_("Credit/Accrual Account is missing for Overhead Type: %s") % ovh_type.name)
                
                display_name = line.product_id.display_name if line.product_id else (ovh_type.name if ovh_type else _('Overhead'))
                move_vals = {
                    'journal_id': journal.id,
                    'date': fields.Date.context_today(self),
                    'ref': _('Overhead Cost for MO: %s - %s', self.name, display_name),
                    'mrp_production_overhead_id': self.id,
                    'line_ids': [
                        (0, 0, {
                            'name': _('Overhead Debit: %s', display_name),
                            'account_id': debit_account.id,
                            'debit': actual_cost,
                            'credit': 0.0,
                        }),
                        (0, 0, {
                            'name': _('Overhead Credit: %s', display_name),
                            'account_id': credit_account.id,
                            'debit': 0.0,
                            'credit': actual_cost,
                        }),
                    ]
                }
                move = AccountMove.create(move_vals)
                move.action_post()
                line.move_id = move.id

    def action_view_main_product_moves(self):
        self.ensure_one()
        main_moves = self.env['account.move'].search([('stock_move_id', 'in', self.move_finished_ids.ids)])
        return {
            'name': _('Main Product Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', main_moves.ids)],
        }

    def action_view_overhead_moves(self):
        self.ensure_one()
        return {
            'name': _('Variable Overhead Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('mrp_production_overhead_id', '=', self.id)],
        }


class AccountMove(models.Model):
    _inherit = 'account.move'

    mrp_production_overhead_id = fields.Many2one('mrp.production', string='Manufacturing Order (Overhead)', ondelete='set null')
