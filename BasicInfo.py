#✔️❌✅

import streamlit as st
from Function import ask_question
yes_no=['Yes','No']
typical_basic_response=["Yes","No","Unsure"]

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
from datetime import date

def BasicInfo():
    global answers
    # Dictionary to store answers
    # Collect user input
    #(answers, key_name, question, input_type="text", options=None, columns=True)
    # Single-selection Filing Status
    current_tax_year=date.today().year-1
    with st.expander("Basic Information ", expanded=False):
        ask_question(answers, "tax_year",
            "Select the Tax Year:",
            input_type="radio",
            options=list(range(current_tax_year, current_tax_year - 5, -1))
        )  
        if answers.get('tax_year') in range(current_tax_year-3, current_tax_year - 5, -1):
             st.warning("⚠️ As they are no longer accepting e-files for this tax year anymore, this will have to be a paper return, meaning you will have to mail in the tax return to the IRS and/or the FTB.")
        ask_question(answers, "name", "First Name", input_type="text")
        ask_question(answers, "email", "Email", input_type="text")
        filings_statuses = ["Single", "Head of Houeshold", "Married Filing Jointly", "Married Filing Separately","Other","Unsure"]
        ask_question(answers, "phone", "Phone Number", input_type="text")
        ask_question(
            answers,
            "filing_status",
            "Select your filing status:",
            input_type="radio",
            options=filings_statuses,
            columns=False
        )
        if answers.get('filing_status') == "Other" or answers.get('filing_status') == "Unsure":
            ask_question(
                answers,
                "filing_status_other",
                "Explain your filing status:",
                input_type="text_input",
            )
        if answers.get('filing_status') == "Married Filing Separately":
            ask_question(
                answers,
                "legally_married",
               f"1) Were you legally married as of December 31, {answers.get('tax_year')}?",
                            input_type="radio",
                options=yes_no,
                help_text="\n\n You are considered married if you were legally seperated under a divorce or separated maintenance agreement decree. \n\n Marriage status does not depend on where a spouse lives."
            )
            if answers.get('legally_married') == "No":
                ask_question(
                    answers,
                    "spouse_died",
        f"4) Did your spouse die in {answers.get('tax_year')-2} or {answers.get('tax_year')-1}?",
                                input_type="radio",
                    options=yes_no
                )
            if answers.get('legally_married') == "Yes":
                ask_question(
                    answers,
                    "file_jointly",
                "2) Do you wish to filing a joint return?",
                                input_type="radio",
                    options=yes_no
                )
                if answers.get('file_jointly') == "Yes":
                        st.warning("✔️ Your filing status is married filing jointly.")
                        return
                if answers.get('file_jointly') == "No" and answers.get('file_jointly') == "No":
                    ask_question(
                        answers,
                        "married_follow_up_questions",
                    f"3) Do all the following apply? \n\n• You file a separate return from your spouse \n\n• You paid more than half the cost of keeping up your home for the required period of time \n\n• Your spouse did not live in your home during the last 6 months of {answers.get('tax_year')} \n\n• Your home was the main home of your child, stepchild, or foster child for more than half the year (a grandchild doesn’t meet this test). For rules applying to birth, death, or temporary absence during the year, see Publication 17 \n\n• You claim an exemption for the child (unless the noncustodial parent claims the child under rules for divorced or separated parents or parents who live apart)",
                                    input_type="radio",
                        options=yes_no
                    )
                    if answers.get('married_follow_up_questions')=="Yes":
                        st.warning("✅ You are considered unmarried and your filing status is head of houseshold.")
                        return
                    if answers.get('married_follow_up_questions')=="No":
                        st.warning("❌ You are considered married and your filing status is married filing seperately which is out of scope.")
                        return
        if answers.get('spouse_died') == "Yes":
            ask_question(
                answers,
                "qualified_surviving_spouse",
                    f"5) Do all of the following apply? \n\n• You were entitled to file a joint return with your spouse for the year your spouse died \n\n• You didn’t remarry before the end of {answers.get('tax_year')} \n\n• You have a child or stepchild who lived with you all year, except for temporary absences or other limited exceptions, and who is your dependent or who would qualify as your dependent except that: he or she does not meet the gross income test, does not meet the joint return test, or except that you may be claimed as a dependent by another taxpayer. Don’t include a grandchild or foster child \n\n• You paid more than half the cost of keeping up the home for {answers.get('tax_year')}",
                            input_type="radio",
                options=yes_no
            )
            if answers.get('qualified_surviving_spouse')=="Yes":
                st.warning("✔️ Your filing status is qualifying surviving spouse.")
                return
        if answers.get('qualified_surviving_spouse')=="No":
            ask_question(
                answers,
                "MFS_HOH_S",
                f"6) Do both of the following apply? \n\n• You paid more than 1/2 the cost of keeping up your home for {answers.get('tax_year')} \n\n• A “qualifying person” lived with you in your home for more than 1/2 the year. If the qualifying person is your dependent parent, your dependent parent does not have to live with you",
                            input_type="radio",
                options=yes_no )
            if answers.get('MFS_HOH_S')=="Yes":
                st.warning("✅ Your filing status is head of houseshold.")
                return
            if answers.get('MFS_HOH_S')=="No":
                st.warning("✅ Your filing status is single.")
                return

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
            ask_question(answers, "health_forms", "Which form(s) do you have?", 
                        input_type="checkbox",
                        options=["1095-A", "1095-B", "1095-C"],
                        columns=True)

        # Coverage type with multiple selection
            ask_question(answers, "coverage_type", "Type of Health Care Coverage",
                        input_type="checkbox",
                        options=["Medi-Cal", "Medicaid", "Medicare", "Employee Sponsored", "Other"],
                        columns=True)
        health_forms=answers.get("health_forms") or []
        health_1095_a=[
                            "Some people in my household are listed on my 1095-A but some members have their own health insurance",
                            "The 1095-A lists someone not on your tax return",
                            "A person on this tax return was enrolled in another taxpyers Marketplace coverage. (The person is listed on a Form 1095-A sent to a taxpayer not on this tax return.)",
                            f"You got married during {answers.get('tax_year')}, were unmarried as of January 1st, {answers.get('tax_year')}, and want to do an alternative calculation for year of marriage.",
                            "You or your spouse are self employed and want to deduct their health insurance premiums."]
        if  "1095-A" in health_forms:
            ask_question(answers, "1095-A_Warning", "Please check any that apply.", 
                        input_type="checkbox",
                        options=health_1095_a
                            ,columns=False,help_text="See Publication 974, 4012 H-14, or ask a VITA volunteer for more details.")
        selected = answers.get("1095-A_Warning", [])
        if any(option in selected for option in health_1095_a[1:]):
            st.warning("❌ Out of scope")
        elif any(option in selected for option in health_1095_a[1]):
            st.warning("✅ In scope")
                                


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
        ask_question(
            answers,
            "EstimatedTaxPayments",
            f"Did you or your spouse make any estimated tax payments throughout {answers.get('tax_year')}?",
            input_type="radio",
            options=typical_basic_response,
            columns=False,
            help_text="Estimated tax payments are periodic payments you make to the government during the year on income that isn’t automatically taxed through withholding, such as self employment."
        )
        if answers.get("EstimatedTaxPayments") == "Yes":
            tax_year = answers.get("tax_year")
            quarters = [
                (f"Q1 - April 15, {tax_year}", f"Q1_{tax_year}"),
                (f"Q2- June 15, {tax_year}", f"Q2_{tax_year}"),
                (f"Q3 - September 15, {tax_year}", f"Q3_{tax_year}"),
                (f"Q4 - January 15, {tax_year+1}", f"Q4_{tax_year+1}")
            ]
            answers.setdefault("EstimatedTax", {})
            for label, key in quarters:
                st.write(f"### {label}")
                col1, col2 = st.columns(2)
                with col1:
                    answers["EstimatedTax"][f"{key}_FD"] = st.number_input(
                        f"Federal (FD) - {label}",
                        min_value=0,
                        step=50,
                        key=f"fd_{key}"
                    )
                with col2:
                    answers["EstimatedTax"][f"{key}_CA"] = st.number_input(
                        f"California (CA) - {label}",
                        min_value=0,
                        step=50,
                        key=f"ca_{key}"
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
        if answers.get("1099-R") =="Yes":
            ask_question(
                answers,
                "code_7_no_ira",
                "Do all your 1099-R forms have code 7 in box 7 AND the IRA/SEP/SIMPLE box is NOT checked?",
                input_type="radio",
                options=typical_basic_response,
                columns=False
            )
            if answers.get("code_7_no_ira") == "Yes":
                st.success("✅ In Scope")
                return
            else:
                ask_question(
                    answers,
                    "1099_R_Conversions",
                    "Do any of your 1099-R forms involve a traditional IRA to ROTH IRA conversion?",
                    input_type="radio",
                    options=typical_basic_response,
                    columns=False
                )
                if answers.get("1099_R_Conversions") == "Yes":
                    st.warning("❌ Out of Scope")
                    return
                if answers.get("1099_R_Conversions") == "No":
                    ask_question(
                        answers,
                        "code_1",
                        "Do any of your 1099-R forms have code 1 in box 7?",
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
                        st.success("✅ In Scope")
                        return
                    if answers.get("code_1") == "No":
                        ask_question(
                            answers,
                            "bad_codes",
                            "Do any of your 1099-R forms have any of these codes in box 7: 5, 8, 9, A, E, J, K, N, P, R, T, U?",
                            input_type="radio",
                            options=typical_basic_response,
                            columns=False
                        )
                        if answers.get("bad_codes") == "Yes":
                            st.warning("❌ Out of Scope")
                            return

                        # ----------------------------
                        # Q4: Code 2 or 7 + IRA + nondeductible
                        # ----------------------------
                        ask_question(
                            answers,
                            "code_2_or_7_ira_nondeduct",
                            "Do any of your 1099-R formsr have code 2 or 7 in box 7 AND IRA/SEP/SIMPLE box checked AND you made nondeductible contributions?",
                            input_type="radio",
                            options=typical_basic_response,
                            columns=False
                        )

                        if answers.get("code_2_or_7_ira_nondeduct") == "Yes":
                            st.warning("❌ Out of Scope")
                            return
                        
                        ask_question(
                            answers,
                            "code_2",
                            "Do any of your 1099-R forms have code 2 in box 7?",
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
                                st.warning("❌ Out of Scope")
                                return
                            if answers.get("code_2_ira_nondeduct") == "No":
                                st.warning("✅ In Scope")
                                return

                        # ----------------------------
                        # Q6: Code 4 (Death)
                        # ----------------------------
                        ask_question(
                            answers,
                            "code_4",
                            "Do any of your 1099-R forms have code 4 in box 7?",
                            input_type="radio",
                            options=typical_basic_response,
                            columns=False
                        )

                        if answers.get("code_4") == "Yes":
                            ask_question(
                                answers,
                                "inherited_ira",
                                "Did they involve an inherited IRA?",
                                input_type="radio",
                                options=typical_basic_response,
                                columns=False
                            )
                            if answers.get("inherited_ira") == "Yes":
                                ask_question(
                                    answers,
                                    "cost_basis",
                                    "For in the inhereited IRA, did it have a cost basis?",
                                    input_type="radio",
                                    options=typical_basic_response,
                                    columns=False
                                )

                                if answers.get("cost_basis") == "Yes":
                                    st.warning("❌ Out of Scope")
                                    return
                                if answers.get("cost_basis") == "No":
                                    st.warning("✅ In Scope")
                                    return;
                            else:
                                st.success("✅ In Scope (Survivor benefits)")
                            return



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
            year_data["tax_year"] = st.text_input(f"Tax Year (Year #{i+1})", key=f"SSA_Lump_Sum_year_{i}")
            year_data["filing_status"] = st.selectbox(
                f"Filing Status for that year",
                ["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"],
                key=f"SSA_Lump_Sum_status_{i}"
            )
            year_data["ssa_received"] = st.number_input(
                f"Total Social Security received that year",
                min_value=0.0,
                step=100.0,
                key=f"SSA_Lump_Sum_total_received_{i}"
            )
            year_data["lump_sum_amount"] = st.number_input(
                f"Portion of THIS year’s benefits for that year ($)",
                min_value=0.0,
                step=100.0,
                key=f"SSA_Lump_Sum_portio_{i}"
            )
            year_data["agi"] = st.number_input(
                f"AGI for that year (Form 1040 Line 11)",
                min_value=0.0,
                step=100.0,
                key=f"SSA_Lump_Sum_agi_{i}"
            )
            year_data["adjustments"] = st.number_input(
                f"Adjustments/Exclusions (Form 1040 Line 10)",
                min_value=0.0,
                step=100.0,
                key=f"SSA_Lump_Sum_adjustments_{i}"
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
                key=f"SSA_Lump_Sum_taxable_ssa_{i}"
            )
        answers["ssa_lump_sum_details"].append(year_data)
        st.success("✔️ Lump sum Social Security details captured")

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
                        index=None,
                        key=f"business_type_{i}"
                    )
                    if year_data["business_type"] == "Other":
                        year_data["other_business"] = st.text_input("Describe your business:", key=f"SCH_C_other_business_descr_{i}")
                    year_data["1099_nec_amounts"] = st.number_input(
                        "Number of 1099-NEC forms:",min_value=0,
                        step=1,
                        key=f"SCH_C_1099_nec_{i}"
                    )
                    year_data["1099_k_amounts"] = st.number_input(
                        "Number of 1099-K forms:",min_value=0,
                        step=1,
                        key=f"SCH_C_1099_k_{i}"
                    )
                    year_data["1099_misc_amounts"] = st.number_input(
                        "Number of 1099-Misc forms:",min_value=0,
                        step=1,
                        key=f"SCH_C_1099_misc_{i}"
                    )
                    year_data["other_cash_income"] = st.number_input(
                        "Other cash income ($)",step=50,
                        key=f"SCH_C_cash_income_{i}"
                    )
                    st.subheader("Business Expenses")            
                    year_data["advertising"] = st.number_input("Advertising ($)", step=50, key=f"SCH_C_advertising_{i}")
                    year_data["contract_labor"] = None  # No input, out of scope
                    st.info("Contract Labor is out of scope.")
                    year_data["commission_and_fees"] = st.number_input("Commission and Fees ($)", step=50, key=f"SCH_C_commission_and_fees_{i}")
                    year_data["depletion"] = None
                    st.info("Depletion is out of scope.")
                    year_data["employee_benefits"] = None
                    st.info("Employee Benefits is out of scope.")
                    year_data["health_insurance"] = st.number_input("Health Insurance ($)", step=50, key=f"SCH_C_health_insurance_{i}")
                    year_data["insurance_other_than_health"] = st.number_input("Insurance (other than health) ($)", step=50, key=f"SCH_C_insurance_other_than_health_{i}")
                    year_data["mortgage_interest"] = None
                    st.info("Mortgage Interest is out of scope.")
                    year_data["legal_and_professional_services"] = st.number_input("Legal and Professional Services ($)", step=50, key=f"SCH_C_legal_and_professional_services_{i}")
                    year_data["office_expenses"] = st.number_input("Office Expenses ($)", step=50, key=f"SCH_C_office_expenses_{i}")
                    year_data["pension_and_profit_sharing"] = None
                    st.info("Pension and Profit Sharing is out of scope.")
                    year_data["rent_or_lease_of_equipment"] = st.number_input("Rent or Lease of Equipment ($)", step=50, key=f"SCH_C_rent_or_lease_of_equipment_{i}")
                    year_data["rent_or_lease_of_property"] = st.number_input("Rent or Lease of Property ($)", step=50, key=f"SCH_C_rent_or_lease_of_property_{i}")
                    year_data["repairs_and_maintenance"] = st.number_input("Repairs and Maintenance ($)", step=50, key=f"SCH_C_repairs_and_maintenance_{i}")
                    year_data["supplies"] = st.number_input("Supplies ($)", step=50, key=f"SCH_C_supplies_{i}")
                    year_data["taxes_and_licenses"] = st.number_input("Taxes and Licenses ($)", step=50, key=f"tSCH_C_axes_and_licenses_{i}")
                    year_data["travel"] = st.number_input("Travel ($)", step=50, key=f"SCH_C_travel_{i}")
                    year_data["meals_and_entertainment"] = None
                    st.info("Meals and Entertainment is out of scope.")            
                    year_data["utilities"] = st.number_input("Utilities ($)", step=50, key=f"SCH_C_utilities_{i}")
                    year_data["wages"] = st.number_input("Wages ($)", step=50, key=f"SCH_C_wages_{i}")
                    year_data["other_expenses"] = st.number_input("Other Expenses ($)", step=50, key=f"SCH_C_other_expenses_{i}")
                    # Car and truck expenses
                    st.subheader("Car and Truck Expenses")
                ask_question(
                    year_data,
                    key_name=f"SCH_C_vehicle_desc_{i}",
                    question="Description of Vehicle:",
                    input_type="text"
                )

                ask_question(
                    year_data,
                    key_name=f"SCH_C_vehicle_date_{i}",
                    question="Date vehicle placed in service:",
                    input_type="date"
                )

                year_data["miles"] = st.number_input("Bussiness Miles", step=50, key=f"SCH_C_Miles_{i}",help="Do not include commuting mileage.")
                ask_question(
                    year_data,
                    key_name=f"SCH_C_vehicle_other_{i}",
                    question="Do you or your spouse have another vehicle available for personal use?",
                    input_type="radio",
                    options=["Yes", "No"]
                )

                ask_question(
                    year_data,
                    key_name=f"SCH_C_vehicle_off_duty_{i}",
                    question="Was this vehicle available for personal use during off-duty hours?",
                    input_type="radio",
                    options=["Yes", "No"]
                )

                ask_question(
                    year_data,  
                    key_name=f"SCH_C_vehicle_evidence_{i}",
                    question="Do you have evidence to support your deduction?",
                    input_type="radio",
                    options=["Yes", "No"]
                )

                # Conditional question if evidence exists
                if year_data.get(f"SCH_C_vehicle_evidence_{i}") == "Yes":
                    ask_question(
                        year_data,
                        key_name=f"SCH_C_vehicle_written_{i}",
                        question="Is the evidence written?",
                        input_type="radio",
                        options=["Yes", "No"]
                    )
                                # Append year/business data to answers
                answers["schedule_c_details"].append(year_data)

def SchD():
    global answers, yes_no, typical_basic_response
    with st.expander("Sale of Capital Assets", expanded=False):
        ask_question(
            answers,
            key_name="sold_stocks_or_etfs",
            question="Did you sell stocks, mutual funds, or ETFs outside a retirement account?",
            input_type="radio",
            options=typical_basic_response
        )
        ask_question(
            answers,
            key_name="transactions",
            question="Did you have transactions involving options, futures, or commodities?",
            input_type="radio",
            options=typical_basic_response
        )
        if answers.get('transactions') == "Yes":
            st.warning("❌ Out of scope.")
            return
        ask_question(
            answers,
            key_name="crypto",
            question="Did you sell any cyptocurrency assets or earn any cryptocurrency income (1099-DA)?",
            input_type="radio",
            options=typical_basic_response
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
            options=typical_basic_response
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
            options=typical_basic_response
            )
        if answers.get('complex_basis') == "Yes":
                st.warning("❌ Out of scope.")
                return
        st.warning ("✔️ In scope.")


def Deductions():
    global answers, yes_no, typical_basic_response
    with st.expander("Student Loan Interest: 1098-E", expanded=False):
        ask_question(
            answers,
            key_name="student_loan_interest",
            question="You or your spouse pay any student loan interest?",
            input_type="radio",
            options=typical_basic_response
        )
        if answers.get('student_loan_interest') == "Yes":
             st.warning("✅ In scope, lease have your 1098-E forms handy.")
    with st.expander("Qualified Educator", expanded=False):
        ask_question(
                answers,
                key_name="qualified_educator",
                question="You or your spouse a K-12 teacher, instructor, counselor, aide, or principal who worked at least 900 hours during the school year?",
                input_type="radio",
                options=typical_basic_response
            )
        if answers.get('qualified_educator') == "Yes":
            ask_question(
                answers,
                key_name="educator_amount",
                question="How much did you spend on out of pocket clasroom expenses? ($)",
                input_type="number",step=50
            )


