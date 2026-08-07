# -*- coding: utf-8 -*-
from odoo import models, api

class BomOverheadReport(models.AbstractModel):
    _name = 'report.advance_mrp_costing_ucs.report_bom_overhead'
    _description = 'BOM Material & Overhead Cost Report Parser'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.bom'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'mrp.bom',
            'docs': docs,
        }
