# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    overhead_type_id = fields.Many2one('mrp.overhead.type', string='Overhead Type', help='Assign Overhead Type to service product items used for extra manufacturing costs.')
