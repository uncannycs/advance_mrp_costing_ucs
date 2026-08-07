# -*- coding: utf-8 -*-
{
    'name': 'Advance Costing & MRP | Manufacturing Overhead Costs | Variable & Fixed MRP Costs | Bill of Materials Costing | Unbuild Extra Costs | Kit Delivery Accounting | Manufacturing Cost Deviation Reports',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Advanced MRP Costing, Variable & Fixed Overhead Cost Control, Unbuild Extra Costs, Kit Delivery Accounting & Reports',
    'description': """
Advance MRP Costing and Total Accounting Solution
=================================================
This module provides a complete solution for managing direct and indirect overhead costs 
(such as labor, electricity, machine depreciation, tooling, and freight) in Odoo Manufacturing (MRP).

Key Features:
-------------
* Overhead Type Configuration with Expense and Credit GL Account mapping.
* Assign Overhead Types to Service Products.
* Bill of Materials (BOM) Variable & Fixed Overhead Cost Calculation with Costing summary.
* Manufacturing Order (MO) Overhead tracking, Cost Variance calculation, and automated Accounting Entries.
* Unbuild Orders extra cost calculation and reversal Journal Entries.
* Kit Delivery & Kit Picking accounting, quantity adjustment wizard, and Kit Delivery Slip PDF report.
* Multidimensional Pivot and Graph analytics for BOM Overhead Details, MRP Overhead Details, and Kit Pickings.
* Comprehensive PDF Reports: BOM Material & Overhead Cost, MRP Material & Overhead Cost, MRP Deviation Report, MRP Estimate Cost Report, and Kit Delivery Slip.
    """,
    'author': 'Uncanny Consulting Services LLP',
    'website': 'https://uncannycs.com',
    'license': 'Other proprietary',
    'price': 60,
    'currency': 'USD',
    'images': ['static/description/banner.gif'],
    'depends': [
        'mrp',
        'stock',
        'account',
        'stock_account',
        'sale_management',
    ],
    'data': [
        'security/mrp_extra_cost_security.xml',
        'security/ir.model.access.csv',
        'wizard/update_kit_qty_wizard_view.xml',
        'views/mrp_overhead_type_views.xml',
        'views/product_template_views.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_unbuild_views.xml',
        'views/stock_picking_views.xml',
        'views/mrp_overhead_analysis_views.xml',
        'views/menu_items.xml',
        'report/bom_overhead_report_template.xml',
        'report/mrp_overhead_report_template.xml',
        'report/mrp_deviation_report_template.xml',
        'report/mrp_estimate_cost_report_template.xml',
        'report/kit_delivery_slip_template.xml',
        'report/report_actions.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
