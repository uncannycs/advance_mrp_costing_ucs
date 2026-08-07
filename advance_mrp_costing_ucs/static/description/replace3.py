import re

with open('/home/thinkpad3/workspace/17.0/custom/apps/advance_mrp_costing_ucs/static/description/index.html', 'r') as f:
    content = f.read()

screenshots_start = content.find('<!-- DESCRIPTION TAB -->')
screenshots_end = content.find('<!-- WHY UNCANNY TAB -->', screenshots_start)

new_screenshots_tab = """<!-- DESCRIPTION TAB -->
                <div aria-labelledby="screenshots-tab" class="tab-pane fade" id="screenshots" role="tabpanel">
                    <div class="mb-5 pt-4">
                        <h1 class="mb-5"
                            style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 40px; text-align: center; color: #171618">
                            See It In
                            <span style="color: #03305A">Action</span>
                        </h1>
                        <!-- Screenshot 1 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3">
                            <div class="col-lg-4">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Configure Overhead Cost Types and Assign GL Accounts
                                    </h2>
                                </div>
                            </div>
                            <div class="col-lg-8">
                                <img alt="Step 1" class="img-fluid w-100 shadow" src="img_1.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                        </div>
                        <!-- Screenshot 2 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3"
                            style="background-color: #fafafa; border-radius: 16px">
                            <div class="col-lg-8 order-2 order-lg-1">
                                <img alt="Step 2" class="img-fluid w-100 shadow" src="img_2.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                            <div class="col-lg-4 order-1 order-lg-2">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Assign Variable Overheads to Bills of Materials
                                    </h2>
                                </div>
                            </div>
                        </div>
                        <!-- Screenshot 3 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3">
                            <div class="col-lg-4">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Track Costs on Manufacturing Orders
                                    </h2>
                                </div>
                            </div>
                            <div class="col-lg-8">
                                <img alt="Step 3" class="img-fluid w-100 shadow" src="img_3.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                        </div>
                        <!-- Screenshot 4 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3"
                            style="background-color: #fafafa; border-radius: 16px">
                            <div class="col-lg-8 order-2 order-lg-1">
                                <img alt="Step 4" class="img-fluid w-100 shadow" src="img_4.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                            <div class="col-lg-4 order-1 order-lg-2">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Automated Journal Entries on MO Completion
                                    </h2>
                                </div>
                            </div>
                        </div>
                        <!-- Screenshot 5 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3">
                            <div class="col-lg-4">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Unbuild Extra Cost Reversals
                                    </h2>
                                </div>
                            </div>
                            <div class="col-lg-8">
                                <img alt="Step 5" class="img-fluid w-100 shadow" src="img_5.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                        </div>
                        <!-- Screenshot 6 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3"
                            style="background-color: #fafafa; border-radius: 16px">
                            <div class="col-lg-8 order-2 order-lg-1">
                                <img alt="Step 6" class="img-fluid w-100 shadow" src="img_6.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                            <div class="col-lg-4 order-1 order-lg-2">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Kit Deliveries and Operations
                                    </h2>
                                </div>
                            </div>
                        </div>
                        <!-- Screenshot 7 -->
                        <div class="row mx-auto px-md-5 px-2 my-lg-4 my-2 py-5 row-gap-3">
                            <div class="col-lg-4">
                                <div class="d-flex h-100 justify-content-center align-items-center flex-column">
                                    <h2 class="text-start w-100 mb-0"
                                        style="font-family: 'Montserrat', sans-serif; color: #060506; font-size: calc(1.1rem + 1vw); font-weight: 500">
                                        Audit-Ready PDF Reports for Analysis
                                    </h2>
                                </div>
                            </div>
                            <div class="col-lg-8">
                                <img alt="Step 7" class="img-fluid w-100 shadow" src="img_7.png"
                                    style="border: 3.6px solid #4c5562; border-radius: 16px; object-fit: cover">
                            </div>
                        </div>
                    </div>
                </div>
                
                """

if screenshots_start != -1 and screenshots_end != -1:
    content = content[:screenshots_start] + new_screenshots_tab + content[screenshots_end:]

with open('/home/thinkpad3/workspace/17.0/custom/apps/advance_mrp_costing_ucs/static/description/index.html', 'w') as f:
    f.write(content)

