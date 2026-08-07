# -*- coding: utf-8 -*-
from odoo import models, api

class KitPickingReport(models.AbstractModel):
    _name = 'report.advance_mrp_costing_ucs.report_kit_delivery'
    _description = 'Kit Delivery Slip Report Parser'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': docs,
        }
