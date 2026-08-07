# -*- coding: utf-8 -*-
from odoo import models, api

class MrpOverheadReport(models.AbstractModel):
    _name = 'report.advance_mrp_costing_ucs.report_mrp_overhead'
    _description = 'MRP Cost & Overhead Report Parser'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.production'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'mrp.production',
            'docs': docs,
        }
