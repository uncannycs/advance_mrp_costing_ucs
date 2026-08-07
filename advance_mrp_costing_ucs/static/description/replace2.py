import re

with open('/home/thinkpad3/workspace/17.0/custom/apps/advance_mrp_costing_ucs/static/description/index.html', 'r') as f:
    content = f.read()

# Replace Hot Features section
hot_features_start = content.find('<!-- 6. Hot Features Section -->')
hot_features_end = content.find('<!-- Note Section -->', hot_features_start)

new_hot_features = """<!-- 6. Hot Features Section -->
                    <div class="position-relative row mx-auto justify-content-center py-5">
                        <div class="text-center mb-5">
                            <h3 class="fw-bold" style="font-family: 'Montserrat', sans-serif; color: #03305A; font-size: 30px">Hot Features</h3>
                            <div class="d-flex justify-content-center align-items-center mt-2">
                                <img alt="line" src="images/line.png">
                            </div>
                        </div>
                        <div class="col-12 col-lg-10">
                            <div class="row g-3">
                                <div class="col-12 col-md-4">
                                    <div class="d-flex align-items-center p-3 shadow-sm h-100 hover-shadow"
                                        style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px">
                                        <img alt="icon" src="icons/bolt-blue.svg" style="width: 36px; height: 36px; margin-right: 15px">
                                        <div style="text-align: left">
                                            <span style="font-size: 14px; font-weight: 700; color: #03305A; line-height: 1.2">BOM Variable Overhead Engine</span>
                                            <span class="badge bg-danger ms-1" style="font-size: 9px; padding: 3px 5px; vertical-align: middle; border-radius: 4px">HOT</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="d-flex align-items-center p-3 shadow-sm h-100 hover-shadow"
                                        style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px">
                                        <img alt="icon" src="icons/gears-blue.svg" style="width: 36px; height: 36px; margin-right: 15px">
                                        <div style="text-align: left">
                                            <span style="font-size: 14px; font-weight: 700; color: #03305A; line-height: 1.2">MO Auto Journal Entry Posting</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="d-flex align-items-center p-3 shadow-sm h-100 hover-shadow"
                                        style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px">
                                        <img alt="icon" src="icons/sync-light.svg" style="width: 36px; height: 36px; margin-right: 15px">
                                        <div style="text-align: left">
                                            <span style="font-size: 14px; font-weight: 700; color: #03305A; line-height: 1.2">Unbuild Cost Reversal Moves</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="d-flex align-items-center p-3 shadow-sm h-100 hover-shadow"
                                        style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px">
                                        <img alt="icon" src="icons/chart-line.svg" style="width: 36px; height: 36px; margin-right: 15px">
                                        <div style="text-align: left">
                                            <span style="font-size: 14px; font-weight: 700; color: #03305A; line-height: 1.2">Planned vs Actual Variance Analysis</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="d-flex align-items-center p-3 shadow-sm h-100 hover-shadow"
                                        style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px">
                                        <img alt="icon" src="icons/shield.svg" style="width: 36px; height: 36px; margin-right: 15px">
                                        <div style="text-align: left">
                                            <span style="font-size: 14px; font-weight: 700; color: #03305A; line-height: 1.2">Kit Picking Quantity Wizard</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 col-md-4">
                                    <div class="d-flex align-items-center p-3 shadow-sm h-100 hover-shadow"
                                        style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px">
                                        <img alt="icon" src="icons/chart-pie-blue.svg" style="width: 36px; height: 36px; margin-right: 15px">
                                        <div style="text-align: left">
                                            <span style="font-size: 14px; font-weight: 700; color: #03305A; line-height: 1.2">5 Audit-Ready QWeb PDF Reports</span>
                                            <span class="badge bg-danger ms-1" style="font-size: 9px; padding: 3px 5px; vertical-align: middle; border-radius: 4px">HOT</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    """

if hot_features_start != -1 and hot_features_end != -1:
    content = content[:hot_features_start] + new_hot_features + content[hot_features_end:]


# Replace Features Tab section
features_start = content.find('<!-- FEATURES TAB -->')
features_end = content.find('<!-- DESCRIPTION TAB -->', features_start)

new_features_tab = """<!-- FEATURES TAB -->
                <div aria-labelledby="features-tab" class="tab-pane fade" id="features" role="tabpanel">
                    <div class="row justify-content-center mx-auto my-5 py-5 rounded-4" style="background-color: #f8f9fa">
                        <div class="col-12 text-center mb-5">
                            <h1 class="mb-3" style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 36px; color: #171618">
                                Explore The <span style="color: #03305A">Key Features</span>
                            </h1>
                            <p class="text-muted" style="font-size: 16px">Comprehensive extra cost tracking and accounting for your manufacturing plant.</p>
                        </div>
                        <div class="col-12 col-lg-10">
                            <div class="row g-4">
                                <div class="col-md-6">
                                    <div class="d-flex p-4 bg-white rounded-4 shadow-sm h-100 hover-shadow" style="border: 1px solid #e5e7eb">
                                        <div class="flex-shrink-0 me-4">
                                            <div class="d-flex align-items-center justify-content-center rounded-3" style="width: 50px; height: 50px; background-color: #e9f2fb">
                                                <img alt="icon" src="icons/gears-blue.svg" style="width: 24px; height: 24px">
                                            </div>
                                        </div>
                                        <div>
                                            <h5 class="fw-bold text-dark mb-2" style="font-family: 'Montserrat', sans-serif; font-size: 18px">Overhead Type Master</h5>
                                            <p class="text-muted mb-0" style="font-size: 14px; line-height: 1.6">Map cost categories (Labor, Power, Depreciation, Tooling) to GL Debit Expense accounts and Credit Accrual accounts.</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex p-4 bg-white rounded-4 shadow-sm h-100 hover-shadow" style="border: 1px solid #e5e7eb">
                                        <div class="flex-shrink-0 me-4">
                                            <div class="d-flex align-items-center justify-content-center rounded-3" style="width: 50px; height: 50px; background-color: #e9f2fb">
                                                <img alt="icon" src="icons/bolt-blue.svg" style="width: 24px; height: 24px">
                                            </div>
                                        </div>
                                        <div>
                                            <h5 class="fw-bold text-dark mb-2" style="font-family: 'Montserrat', sans-serif; font-size: 18px">Flexible Costing Basis</h5>
                                            <p class="text-muted mb-0" style="font-size: 14px; line-height: 1.6">Configure extra costs as Fixed Amounts, Per Unit Produced, or Percentage of Material Cost on BOM overhead lines.</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex p-4 bg-white rounded-4 shadow-sm h-100 hover-shadow" style="border: 1px solid #e5e7eb">
                                        <div class="flex-shrink-0 me-4">
                                            <div class="d-flex align-items-center justify-content-center rounded-3" style="width: 50px; height: 50px; background-color: #e9f2fb">
                                                <img alt="icon" src="icons/chart-line.svg" style="width: 24px; height: 24px">
                                            </div>
                                        </div>
                                        <div>
                                            <h5 class="fw-bold text-dark mb-2" style="font-family: 'Montserrat', sans-serif; font-size: 18px">Planned vs. Actual Variance</h5>
                                            <p class="text-muted mb-0" style="font-size: 14px; line-height: 1.6">Track material &amp; overhead cost deviations on MOs to pinpoint production inefficiencies and cost overruns.</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex p-4 bg-white rounded-4 shadow-sm h-100 hover-shadow" style="border: 1px solid #e5e7eb">
                                        <div class="flex-shrink-0 me-4">
                                            <div class="d-flex align-items-center justify-content-center rounded-3" style="width: 50px; height: 50px; background-color: #e9f2fb">
                                                <img alt="icon" src="icons/sync-light.svg" style="width: 24px; height: 24px">
                                            </div>
                                        </div>
                                        <div>
                                            <h5 class="fw-bold text-dark mb-2" style="font-family: 'Montserrat', sans-serif; font-size: 18px">Unbuild Overhead Reversal</h5>
                                            <p class="text-muted mb-0" style="font-size: 14px; line-height: 1.6">Automatically post credit/debit reversal journal entries whenever products are unbuilt back into raw materials.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                """

if features_start != -1 and features_end != -1:
    content = content[:features_start] + new_features_tab + content[features_end:]

with open('/home/thinkpad3/workspace/17.0/custom/apps/advance_mrp_costing_ucs/static/description/index.html', 'w') as f:
    f.write(content)

