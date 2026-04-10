import streamlit as st
from Function import ask_question
yes_no=['Yes','No']
answers={}
def Disclaimers():
    with st.expander("Disclaimer", expanded=False):
        st.write("This questionnaire is intended to augment the VITA interview process, not replace it.")
        st.write("It will ask you basic questions about deductions, income, credits, and your personal tax situation.")
        st.write("It also screens for out-of-scope scenarios for VITA services.")
        st.write("All information you provide is **confidential** and will only be used for preparing your tax questionnaire.")
        st.write("Please answer questions as accurately as possible.")

def RequiredDocuments():
    with st.expander("Required Documents", expanded=False):
        st.write("Before you start, please gather the following documents to complete this questionnaire accurately:")
        st.write("- **Photo ID** (Driver's license, state ID, or passport)")
        st.write("- **Social Security Card** or ITIN documentation for yourself and dependents")
        st.write("- **Income Documents** (W-2s, 1099s, unemployment forms, etc.)")
        st.write("- **Deduction & Credit Documentation** (receipts for charitable donations, education expenses, medical expenses, child care expenses, etc.)")
        st.write("- **Health Insurance Information** (Form 1095-A, 1095-B, or 1095-C)")
        st.write("- **Previous Year Tax Return** (optional, but helpful for reference)")
        st.write("Having these documents ready will help you complete the questionnaire faster and ensure accurate reporting.")


def BasicInfo():
    global answers
    # Dictionary to store answers
    # Collect user input
    #(answers, key_name, question, input_type="text", options=None, columns=True)
    # Single-selection Filing Status
    with st.expander("Basic Information ", expanded=False):
        ask_question(answers, "name", "First Name", input_type="text")
        ask_question(answers, "email", "Email", input_type="text")
        filings_statuses = ["Single", "Head of Houeshold", "Married Filing Jointly", "Married Filing Separately"]
        ask_question(answers, "phone", "Phone Number", input_type="text")
        ask_question(
            answers,
            "filing_status",
            "Select your filing status:",
            input_type="radio",
            options=filings_statuses,
            columns=False,
            allow_none=True
        )
        if answers.get('filing_status') == "Married Filing Separately":
                    st.warning("⚠️ Married Filing Separately may be out of scope for VITA services.")

def HealthInsurance():
    global answers
    with st.expander("Health Insurance", expanded=False):
        health_insurance_responses=["Yes, everyone in my houeshold had coverage all year", 
                "Yes, some members in my household had health insurance for part or all of the year", 
                 "No, no one in my household had any health insurance during the year", 
                 "I am unsure"]
        ask_question(
            answers,
            "insurance_status",
            "Did you have health insurance for any member of your household?",
            input_type="radio",
            options=health_insurance_responses,
            columns=False,  # important
            help_text="Household includes you, your spouse (if married), and anyone you claim as a dependent on your tax return."
        )
        if answers.get("insurance_status") in health_insurance_responses[0:2]:
            ask_question(answers, "forms", "Which form(s) do you have?", 
                        input_type="checkbox",
                        options=["1095-A", "1095-B", "1095-C"],
                        columns=True)

        # Coverage type with multiple selection
            ask_question(answers, "coverage_type", "Type of Health Care Coverage",
                        input_type="checkbox",
                        options=["Medi-Cal", "Medicaid", "Medicare", "Employee Sponsored", "Other"],
                        columns=True)

typical_basic_response=["Yes","No","Unsure"]

def CaResidency():
    global answers
    global typical_basic_response
    with st.expander("Residency Questions", expanded=False):        
        ask_question(
            answers,
            "renter_status",
            "Last year, did you rent in California for at least 6 months or more?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )
        ca_residency=["I lived in Califorina for the whole year",
                     "I lived in Califorina for the part of the year but at least 6 months",
                     "I lived in Califorina for the part of the year but not at least 6 months",
                    "Unsure"]
        ask_question(
            answers,
            "ca_residency",
            "Which of the following best describes your living situation last year?",
            input_type="radio",
            options=ca_residency,
            columns=False
        )
        if answers.get("ca_residency") ==  ca_residency[2]:
           st.write("⚠️ You may be required to fill out another state return of which, this site will not be able to assist you in filing state taxes other than California.")

def MiscQuestions():
    global answers
    global typical_basic_response
    with st.expander("Miscallenous Questions", expanded=False):        
        ask_question(
            answers,
            "IHSS",
            "Are you an In Home Supportive Services (IHSS) provider?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )
        if answers.get("IHSS") ==  "Yes":
            ask_question(
                answers,
                "IHSS_live_with_anyone",
                "For IHSS, did you live with anyone you took care of?",
                input_type="radio",
                options=typical_basic_response,
                columns=False
            )
        ask_question(
            answers,
            "IPPIN",
            "Do you or your spouse have an IRS issued IPPIN?",
            input_type="radio",
            options=typical_basic_response,
            columns=False,
            help_text="An IPPIN is a six-digit number the IRS issues to taxpayers to help prevent someone else from filing a fraudulent tax return using your Social Security number."
        )
        
def Income():
    st.write("This section screens for uncommon, out-of-scope scenarios and helps prepare for the intake interview.")
    st.write("Common items like W-2s, dividends, and interest are generally in scope.")
    
def F1099R():
    global answers
    global typical_basic_response
    with st.expander("Distributions: 1099-R", expanded=False):        
        ask_question(
            answers,
            "1099-R",
            "Do you or your spouse have distributions from a retirment account? (1099-R)",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("1099-R") != "Yes":
            return  # no 1099-R, skip section

        # ----------------------------
        # Q1: Code 7, IRA unchecked
        # ----------------------------
        ask_question(
            answers,
            "code_7_no_ira",
            "Does your 1099-R have code 7 in box 7 AND the IRA/SEP/SIMPLE box is NOT checked?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("code_7_no_ira") == "Yes":
            st.success("✅ In Scope – Stop here")
            return

        # ----------------------------
        # Q2: Code 1
        # ----------------------------
        ask_question(
            answers,
            "code_1",
            "Does your 1099-R have code 1 in box 7?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("code_1") == "Yes":
            ask_question(
                answers,
                "code_1_use",
                "What were the distribution funds used for?",
                input_type="text"
            )
            st.success("✅ In Scope – Stop here")
            return

        # ----------------------------
        # Q3: Out-of-scope codes
        # ----------------------------
        ask_question(
            answers,
            "bad_codes",
            "Does your 1099-R have any of these codes in box 7: 5, 8, 9, A, E, J, K, N, P, R, T, U?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("bad_codes") == "Yes":
            st.error("❌ Out of Scope – Stop here")
            return

        # ----------------------------
        # Q4: Code 2 or 7 + IRA + nondeductible
        # ----------------------------
        ask_question(
            answers,
            "code_2_or_7_ira_nondeduct",
            "Does your 1099-R have code 2 or 7 in box 7 AND IRA/SEP/SIMPLE box checked AND you made nondeductible contributions?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("code_2_or_7_ira_nondeduct") == "Yes":
            st.error("❌ Out of Scope – Stop here")
            return

        # ----------------------------
        # Q5: Code 2
        # ----------------------------
        ask_question(
            answers,
            "code_2",
            "Does your 1099-R have code 2 in box 7?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("code_2") == "Yes":

            ask_question(
                answers,
                "code_2_ira_nondeduct",
                "Is IRA/SEP/SIMPLE checked AND did you make nondeductible contributions?",
                input_type="radio",
                options=typical_basic_response,
                columns=False
            )

            if answers.get("code_2_ira_nondeduct") == "Yes":
                st.error("❌ Out of Scope – Stop here")
            else:
                st.success("✅ In Scope – Stop here")
            return

        # ----------------------------
        # Q6: Code 4 (Death)
        # ----------------------------
        ask_question(
            answers,
            "code_4",
            "Does your 1099-R have code 4 in box 7?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )

        if answers.get("code_4") == "Yes":

            ask_question(
                answers,
                "inherited_ira",
                "Was it an inherited IRA?",
                input_type="radio",
                options=typical_basic_response,
                columns=False
            )

            if answers.get("inherited_ira") == "Yes":

                ask_question(
                    answers,
                    "cost_basis",
                    "Did it have a cost basis?",
                    input_type="radio",
                    options=typical_basic_response,
                    columns=False
                )

                if answers.get("cost_basis") == "Yes":
                    st.error("❌ Out of Scope – Stop here")
                else:
                    st.success("✅ In Scope – Stop here")

            else:
                st.success("✅ In Scope (Survivor benefits) – Stop here")

            return

        # ----------------------------
        # Final Warning
        # ----------------------------
        st.warning(
            "⚠️ If this distribution was a Traditional IRA → Roth IRA conversion, it is Out of Scope."
        )

def SSA():
    with st.expander("Social Security: SSA-1099", expanded=False):        
        global answers, yes_no
        # Step 1: Do they have SSA at all?
        ask_question(
            answers,
            "has_ssa",
            "Did you or your spouse receive any Social Security benefits (SSA-1099)?",
            input_type="radio",
            options=yes_no,
            columns=False
        )
        if answers.get("has_ssa") != "Yes":
            return
        # Step 2: Lump sum question
        ask_question(
            answers,
            "ssa_prior_year",
            "Does your Social Security form include payments for prior years (lump-sum payments)?",
            input_type="radio",
            options=["Yes","No"],
            columns=False
        )
        if answers.get("ssa_prior_year") is None:
            return
        if answers.get("ssa_prior_year") == "No":
            return
        if answers.get("ssa_prior_year") == "Yes":
            st.warning(
    "⚠️ You must enter details for each prior-year Social Security lump-sum payment as reported on previous tax returns (Form 1040)."
)
        # ----------------------------
        # Number of prior years
        # ----------------------------
        num_years = st.number_input(
            "How many prior years are included?",
            min_value=1,
            max_value=5,
            step=1
        )
        # Store all years data
        answers["ssa_lump_sum_details"] = []
        # ----------------------------
        # Loop per year
        # ----------------------------
        for i in range(int(num_years)):
            st.markdown(f"### 📅 Prior Year #{i+1}")
            year_data = {}
            year_data["tax_year"] = st.text_input(f"Tax Year (Year #{i+1})", key=f"tax_year_{i}")

            year_data["filing_status"] = st.selectbox(
                f"Filing Status for that year",
                ["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"],
                key=f"filing_status_{i}"
            )

            year_data["ssa_received"] = st.number_input(
                f"Total Social Security received that year",
                min_value=0.0,
                step=100.0,
                key=f"ssa_received_{i}"
            )

            year_data["lump_sum_amount"] = st.number_input(
                f"Portion of THIS year’s benefits for that year ($)",
                min_value=0.0,
                step=100.0,
                key=f"lump_sum_{i}"
            )

            year_data["agi"] = st.number_input(
                f"AGI for that year (Form 1040 Line 11)",
                min_value=0.0,
                step=100.0,
                key=f"agi_{i}"
            )

            year_data["adjustments"] = st.number_input(
                f"Adjustments/Exclusions (Form 1040 Line 10)",
                min_value=0.0,
                step=100.0,
                key=f"adjustments_{i}"
            )

            year_data["tax_exempt_interest"] = st.number_input(
                f"Tax-exempt interest (Form 1040 Line 2a)",
                min_value=0.0,
                step=100.0,
                key=f"interest_{i}"
            )

            year_data["taxable_ssa"] = st.number_input(
                f"Taxable Social Security (Form 1040 Line 6b)",
                min_value=0.0,
                step=100.0,
                key=f"taxable_ssa_{i}"
            )

            answers["ssa_lump_sum_details"].append(year_data)

        st.success("✅ Lump sum Social Security details captured")


import streamlit as st
from Function import ask_question
yes_no=['Yes','No']
answers={}
def SchC():
    global answers, yes_no
    with st.expander("Self Employment: Schedule C", expanded=False):
            global answers
            # Step 1: Do they have SSA at all?
            ask_question(
                answers,
                "has_self_employent",
                "Do you have any 1099-Ks, 1099-MISCs, 1099-NECs, or cash income associate with self emloyment?",
                input_type="radio",
                options=yes_no,
                columns=False
            )
            if answers.get("has_self_employent") == "Yes":
                st.warning("⚠️ Businesses with individual asset purchases over \\$2,500, business use of home, expenses over $50,000 or a net loss are out of scope.")
                st.warning("⚠️ You may not enter all expenses related to the upkeep of a vehicle (gas, insurance, maintenance, etc.). To be in scope and you have vehicle related expenses, you may claim the standard mileage deduction of $0.70 per mile.")      
                # Initialize answers dict
                if "schedule_c_details" not in st.session_state:
                    st.session_state["schedule_c_details"] = []
                answers["schedule_c_details"] = st.session_state["schedule_c_details"]
                num_years = st.number_input(
                    "How many prior self-employment businesses do you want to enter? (1 per activity type)",
                    min_value=1,
                    step=1,
                    value=1
                )
                for i in range(int(num_years)):
                    st.markdown(f"### 💼 Self-Employment Year / Business #{i+1}")
                    year_data = {}
                    year_data["business_type"] = st.radio(
                        "Business Description",
                        ["Taxi & limousine service (Uber / Lyft)", "Other"],
                        key=f"business_type_{i}"
                    )
                    if year_data["business_type"] == "Other":
                        year_data["other_business"] = st.text_input("Describe your business:", key=f"other_business_{i}")
                    year_data["1099_nec_amounts"] = st.number_input(
                        "Number of 1099-NEC forms:",min_value=0,
                        step=1,
                        key=f"1099_nec_{i}"
                    )
                    year_data["1099_k_amounts"] = st.number_input(
                        "Number of 1099-K forms:",min_value=0,
                        step=1,
                        key=f"1099_k_{i}"
                    )
                    year_data["1099_misc_amounts"] = st.number_input(
                        "Number of 1099-Misc forms:",min_value=0,
                        step=1,
                        key=f"1099_misc_{i}"
                    )
                    year_data["other_cash_income"] = st.number_input(
                        "Other cash income ($)",step=50,
                        key=f"cash_income_{i}"
                    )
                    st.subheader("Business Expenses")            
                    year_data["advertising"] = st.number_input("Advertising ($)", step=50, key=f"advertising_{i}")
                    year_data["contract_labor"] = None  # No input, out of scope
                    st.info("Contract Labor is out of scope.")
                    year_data["commission_and_fees"] = st.number_input("Commission and Fees ($)", step=50, key=f"commission_and_fees_{i}")
                    year_data["depletion"] = None
                    st.info("Depletion is out of scope.")
                    year_data["employee_benefits"] = None
                    st.info("Employee Benefits is out of scope.")
                    year_data["health_insurance"] = st.number_input("Health Insurance ($)", step=50, key=f"health_insurance_{i}")
                    year_data["insurance_other_than_health"] = st.number_input("Insurance (other than health) ($)", step=50, key=f"insurance_other_than_health_{i}")
                    year_data["mortgage_interest"] = None
                    st.info("Mortgage Interest is out of scope.")
                    year_data["legal_and_professional_services"] = st.number_input("Legal and Professional Services ($)", step=50, key=f"legal_and_professional_services_{i}")
                    year_data["office_expenses"] = st.number_input("Office Expenses ($)", step=50, key=f"office_expenses_{i}")
                    year_data["pension_and_profit_sharing"] = None
                    st.info("Pension and Profit Sharing is out of scope.")
                    year_data["rent_or_lease_of_equipment"] = st.number_input("Rent or Lease of Equipment ($)", step=50, key=f"rent_or_lease_of_equipment_{i}")
                    year_data["rent_or_lease_of_property"] = st.number_input("Rent or Lease of Property ($)", step=50, key=f"rent_or_lease_of_property_{i}")
                    year_data["repairs_and_maintenance"] = st.number_input("Repairs and Maintenance ($)", step=50, key=f"repairs_and_maintenance_{i}")
                    year_data["supplies"] = st.number_input("Supplies ($)", step=50, key=f"supplies_{i}")
                    year_data["taxes_and_licenses"] = st.number_input("Taxes and Licenses ($)", step=50, key=f"taxes_and_licenses_{i}")
                    year_data["travel"] = st.number_input("Travel ($)", step=50, key=f"travel_{i}")
                    year_data["meals_and_entertainment"] = None
                    st.info("Meals and Entertainment is out of scope.")            
                    year_data["utilities"] = st.number_input("Utilities ($)", step=50, key=f"utilities_{i}")
                    year_data["wages"] = st.number_input("Wages ($)", step=50, key=f"wages_{i}")
                    year_data["other_expenses"] = st.number_input("Other Expenses ($)", step=50, key=f"other_expenses_{i}")

                    
                    # Car and truck expenses
                    st.subheader("Car and Truck Expenses")
                ask_question(
                    year_data,
                    key_name=f"vehicle_desc_{i}",
                    question="Description of Vehicle:",
                    input_type="text"
                )

                ask_question(
                    year_data,
                    key_name=f"vehicle_date_{i}",
                    question="Date vehicle placed in service:",
                    input_type="date"
                )

                year_data["miles"] = st.number_input("Bussiness Miles", step=50, key=f"Miles_{i}",help="Do not include commuting mileage.")

                ask_question(
                    year_data,
                    key_name=f"vehicle_other_{i}",
                    question="Do you or your spouse have another vehicle available for personal use?",
                    input_type="radio",
                    options=["Yes", "No"]
                )

                ask_question(
                    year_data,
                    key_name=f"vehicle_off_duty_{i}",
                    question="Was this vehicle available for personal use during off-duty hours?",
                    input_type="radio",
                    options=["Yes", "No"]
                )

                ask_question(
                    year_data,
                    key_name=f"vehicle_evidence_{i}",
                    question="Do you have evidence to support your deduction?",
                    input_type="radio",
                    options=["Yes", "No"]
                )

                # Conditional question if evidence exists
                if year_data.get(f"vehicle_evidence_{i}") == "Yes":
                    ask_question(
                        year_data,
                        key_name=f"vehicle_written_{i}",
                        question="Is the evidence written?",
                        input_type="radio",
                        options=["Yes", "No"]
                    )
                                # Append year/business data to answers
                    answers["schedule_c_details"].append(year_data)

                

import streamlit as st
from Function import ask_question
yes_no=['Yes','No']
answers={}
def SchD():
    global answers, yes_no
    with st.expander("Sale of Capital Assets", expanded=True):
        ask_question(
            answers,
            key_name="sold_stocks_or_etfs",
            question="Did you sell stocks, mutual funds, or ETFs outside a retirement account?",
            input_type="radio",
            options=["Yes", "No"]
        )
        ask_question(
            answers,
            key_name="transactions",
            question="Did you have transactions involving options, futures, or commodities?",
            input_type="radio",
            options=["Yes", "No"]
        )
        if answers.get('transactions') == "Yes":
            st.warning("❌ Out of scope.")
            return
        ask_question(
            answers,
            key_name="crypto",
            question="Did you sell any cyptocurrency assets or earn any cryptocurrency income (1099-DA)?",
            input_type="radio",
            options=["Yes", "No"]
        )
        if answers.get('crypto') == "Yes":
                    st.warning("❌ Out of scope.")
                    return
        if answers.get('sold_stocks_or_etfs') == "Yes":
            ask_question(
            answers,
            key_name="SCH_D_Codes",
            question="Do any of these codes appear on your 1099-B forms? \n\n C, D, N, Q, R, S, X, Y, or Z",
            input_type="radio",
            options=["Yes", "No"]
            )
        if answers.get('SCH_D_Codes') == "Yes":
            st.warning("❌ Out of scope.")
            return
        if answers.get('sold_stocks_or_etfs') == "Yes":
            ask_question(
            answers,
            key_name="complex_basis",
            question="Do you have complex basis adjustments such as cnoncovered securities, unreported cost basis or wash sales (unless wash sale adjustment is reported clearly)?",
            input_type="radio",
            options=["Yes", "No"]
            )
        if answers.get('complex_basis') == "Yes":
                st.warning("❌ Out of scope.")
                return
        st.warning ("In scope.")


        #st.warning("❌ Out of scope if any of the following apply: \n\n 1. You sold digital assets. \n\n 2. Code C, D, N, P, Q R, S, X, Y, or Z appears on your 1099-B. \n\n 3. You had Transactions involving options, futures, or commodities. \n\n 4. Complex basis adjustments or unreported costs bases. \n\n 5. Wash sales unless clearly reported on tax forms.")
        