# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MrpUnbuild(models.Model):
    _inherit = 'mrp.unbuild'

    unbuild_overhead_line_ids = fields.One2many('mrp.unbuild.overhead.line', 'unbuild_id', string='Variable Overhead Items', copy=True)
    unbuild_overhead_move_ids = fields.One2many('account.move', 'mrp_unbuild_overhead_id', string='Unbuild Overhead Moves')
    
    unbuild_main_move_count = fields.Integer(string='Unbuild Main Moves Count', compute='_compute_unbuild_move_counts')
    unbuild_overhead_move_count = fields.Integer(string='Unbuild Overhead Moves Count', compute='_compute_unbuild_move_counts')

    @api.onchange('mo_id')
    def _onchange_mo_id_overhead(self):
        if self.mo_id:
            lines = []
            for ovh in self.mo_id.overhead_line_ids:
                lines.append((0, 0, {
                    'product_id': ovh.product_id.id,
                    'overhead_type_id': ovh.overhead_type_id.id if ovh.overhead_type_id else False,
                    'quantity': ovh.actual_qty,
                    'unit_cost': ovh.unit_cost,
                    'total_cost': ovh.actual_cost,
                }))
            self.unbuild_overhead_line_ids = [(5, 0, 0)] + lines

    @api.depends('unbuild_overhead_move_ids', 'mo_id')
    def _compute_unbuild_move_counts(self):
        for unbuild in self:
            unbuild.unbuild_overhead_move_count = len(unbuild.unbuild_overhead_move_ids)
            main_moves = self.env['account.move'].search([('ref', 'ilike', unbuild.name)])
            unbuild.unbuild_main_move_count = len(main_moves)

    def action_unbuild(self):
        res = super(MrpUnbuild, self).action_unbuild()
        for unbuild in self:
            unbuild._create_unbuild_overhead_accounting_entries()
        return res

    def _create_unbuild_overhead_accounting_entries(self):
        self.ensure_one()
        AccountMove = self.env['account.move']
        for line in self.unbuild_overhead_line_ids:
            if line.total_cost > 0 and not line.move_id:
                ovh_type = line.overhead_type_id or line.product_id.overhead_type_id
                if not ovh_type:
                    continue
                
                journal = ovh_type.journal_id or self.env['account.journal'].search([('type', '=', 'general'), ('company_id', '=', self.company_id.id)], limit=1)
                debit_account = ovh_type.expense_account_id or line.product_id.property_account_expense_id
                credit_account = ovh_type.credit_account_id or line.product_id.property_account_income_id
                
                if not debit_account or not credit_account or not journal:
                    continue
                
                # Reversal entry for unbuilding
                move_vals = {
                    'journal_id': journal.id,
                    'date': fields.Date.context_today(self),
                    'ref': _('Unbuild Overhead Reversal: %s - %s', self.name, line.product_id.display_name),
                    'mrp_unbuild_overhead_id': self.id,
                    'line_ids': [
                        (0, 0, {
                            'name': _('Unbuild Overhead Reversal Credit: %s', line.product_id.display_name),
                            'account_id': debit_account.id,
                            'debit': 0.0,
                            'credit': line.total_cost,
                        }),
                        (0, 0, {
                            'name': _('Unbuild Overhead Reversal Debit: %s', line.product_id.display_name),
                            'account_id': credit_account.id,
                            'debit': line.total_cost,
                            'credit': 0.0,
                        }),
                    ]
                }
                move = AccountMove.create(move_vals)
                move.action_post()
                line.move_id = move.id

    def action_view_unbuild_main_moves(self):
        self.ensure_one()
        main_moves = self.env['account.move'].search([('ref', 'ilike', self.name)])
        return {
            'name': _('Unbuild Main Move Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', main_moves.ids)],
        }

    def action_view_unbuild_overhead_moves(self):
        self.ensure_one()
        return {
            'name': _('Unbuild Overhead Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('mrp_unbuild_overhead_id', '=', self.id)],
        }


class MrpUnbuildOverheadLine(models.Model):
    _name = 'mrp.unbuild.overhead.line'
    _description = 'Unbuild Order Overhead Line'

    unbuild_id = fields.Many2one('mrp.unbuild', string='Unbuild Order', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', string='Overhead Item', domain="[('type', '=', 'service')]", required=True)
    overhead_type_id = fields.Many2one('mrp.overhead.type', string='Overhead Type')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_cost = fields.Float(string='Unit Cost', default=0.0)
    total_cost = fields.Float(string='Total Cost')
    move_id = fields.Many2one('account.move', string='Reversal Journal Entry', readonly=True)


class AccountMoveUnbuild(models.Model):
    _inherit = 'account.move'

    mrp_unbuild_overhead_id = fields.Many2one('mrp.unbuild', string='Unbuild Order (Overhead)', ondelete='set null')
