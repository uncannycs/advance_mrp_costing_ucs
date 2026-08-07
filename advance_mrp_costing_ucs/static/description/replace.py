import re

with open('/home/thinkpad3/Downloads/odoo_track_pod_ucs17/odoo_track_pod_ucs/static/description/index.html', 'r') as f:
    content = f.read()

# Replace titles
content = content.replace('Track POD Integration | Description', 'Advance Costing & MRP | Description')
content = content.replace('Track Pod<br>Integration', 'Advance Costing<br>& MRP')
content = content.replace('Track POD Integration', 'Advance Costing & MRP')
content = content.replace('Track Pod Integration', 'Advance Costing & MRP')

# Replace the "What Sets ... Apart?" description
content = content.replace(
    'The Track POD Integration module connects your Odoo inventory with the Track-POD electronic proof of delivery (ePOD) platform. Once installed, all confirmed outgoing delivery orders (stock pickings) are automatically pushed to Track-POD via a REST API on a scheduled basis — eliminating the need for manual data entry between systems.',
    'Standard Odoo MRP tracks raw material consumption but leaves out critical manufacturing overheads like direct labor, factory electricity, subcontracting, tooling, and indirect expenses. Advance MRP Costing & Total Accounting Solution bridges this gap by providing an end-to-end extra cost engine integrated with Odoo Accounting, complete variance analysis (Planned vs. Actual), Unbuild extra cost reversals, and audit-ready PDF reports.'
)
content = content.replace('You’re just one click away from turning your sales into actionable invoices!', 'Take 100% financial control over your manufacturing operations today!')

# Key Highlights
content = content.replace('Automate delivery order exports to Track-POD with background cron sync.', 'Allocate Fixed, Per-Unit, or Percentage-based manufacturing overheads directly to BOMs & MOs.')
content = content.replace('Save Time', 'Precise Extra Costing')
content = content.replace('Seamlessly sync customer addresses, line goods, volume &amp; weight metrics', 'Automatically generate &amp; post Debit/Credit General Ledger moves on MO Done &amp; Unbuild completion.')
content = content.replace('Real-Time Dispatch', 'Automated Accounting')
content = content.replace('Eliminate manual data entry mistakes between Odoo and Track-POD .', 'Manage kit component picking deliveries, update quantities dynamically, and print kit slips.')
content = content.replace('Ensure Accuracy', 'Kit Delivery &amp; Wizard')


# Screenshots descriptions
# We need to replace the section in "Screenshots" tab (which is Detailed Module Walkthrough).
# Let's just find the whole screenshots-tab div and replace it.
screenshot_section_start = content.find('<div aria-labelledby="screenshots-tab"')
screenshot_section_end = content.find('<!-- WHY UNCANNY TAB -->')

new_screenshot_section = """<div aria-labelledby="screenshots-tab" class="tab-pane fade" id="screenshots" role="tabpanel">
                    <div class="row justify-content-center mx-auto my-5">
                        <div class="col-12 text-center mb-5">
                            <h1 style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 36px; color: #171618">
                                Detailed <span style="color: #03305A">Module Walkthrough</span>
                            </h1>
                        </div>
                        <div class="col-12 col-lg-10">
                            <!-- Step 1 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">1. Configure Overhead Cost Types</h4>
                                <p class="text-muted">Set up manufacturing overhead categories and assign expense &amp; credit ledger accounts for automated accounting posting.</p>
                                <img alt="Step 1" class="img-fluid rounded-3 border" src="img_1.png">
                            </div>
                            <!-- Step 2 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">2. Assign Variable Overheads to Bills of Materials</h4>
                                <p class="text-muted">Define extra overhead lines in the BOM Variable Overhead tab with fixed, per-unit, or percentage calculation bases.</p>
                                <img alt="Step 2" class="img-fluid rounded-3 border" src="img_2.png">
                            </div>
                            <!-- Step 3 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">3. Track Costs on Manufacturing Orders</h4>
                                <p class="text-muted">Manufacturing orders automatically pull BOM overheads and compute actual cost variances.</p>
                                <img alt="Step 3" class="img-fluid rounded-3 border" src="img_3.png">
                            </div>
                            <!-- Step 4 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">4. Automated Journal Entries on MO Completion</h4>
                                <p class="text-muted">Generate and post Debit/Credit General Ledger moves on MO Done completion.</p>
                                <img alt="Step 4" class="img-fluid rounded-3 border" src="img_4.png">
                            </div>
                            <!-- Step 5 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">5. Unbuild Extra Cost Reversals</h4>
                                <p class="text-muted">Automatically reverse extra cost entries when an Unbuild order is completed.</p>
                                <img alt="Step 5" class="img-fluid rounded-3 border" src="img_5.png">
                            </div>
                            <!-- Step 6 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">6. Kit Deliveries</h4>
                                <p class="text-muted">Manage kit component picking deliveries and automate overhead calculations.</p>
                                <img alt="Step 6" class="img-fluid rounded-3 border" src="img_6.png">
                            </div>
                            <!-- Step 7 -->
                            <div class="mb-5 p-4 bg-white rounded-4 shadow-sm border border-light">
                                <h4 class="fw-bold mb-3" style="color: #03305A">7. Audit-Ready PDF Reports</h4>
                                <p class="text-muted">Access comprehensive reports for variance analysis and total overhead costs directly from the Print menu.</p>
                                <img alt="Step 7" class="img-fluid rounded-3 border" src="img_7.png">
                            </div>
                        </div>
                    </div>
                </div>
                
                """

content = content[:screenshot_section_start] + new_screenshot_section + content[screenshot_section_end:]

# Replace Note Section Text
content = content.replace('This app is fully compatible with both Odoo Community and Enterprise Editions. It seamlessly integrates with the standard Sales and Invoicing workflows.', 'This app is fully compatible with both Odoo Community and Enterprise Editions. It seamlessly integrates with core MRP, Stock Valuation, and Accounting apps.')


with open('/home/thinkpad3/workspace/17.0/custom/apps/advance_mrp_costing_ucs/static/description/index.html', 'w') as f:
    f.write(content)

