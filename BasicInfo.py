#🔵✅❌✅⚠️

import streamlit as st
from Function import ask_question
from datetime import date

yes_no=['Yes','No']
typical_basic_response=["Yes","No","Unsure"]
answers={}
pronouns='you'
Pronouns='You'
pronouns2='your'


def Disclaimers():
    with st.expander("Disclaimer", expanded=False):
        st.write("This questionnaire is intended to augment the VITA interview process, not replace it.")
        st.write("It will ask you basic questions about deductions, income, credits, and your personal tax situation.")
        st.write("It also screens for certain out-of-scope scenarios for VITA services.")
        st.write("All information you provide is **confidential** and will only be used for preparing your tax questionnaire.")
        st.write("It will not ask you for SSNs or EINs but please have those handy for the volunteer.")
        st.write("Please answer questions as accurately as possible.")

def RequiredDocuments():
    with st.expander("Required Documents", expanded=False):
        st.write("Before you start, please gather the following documents to complete this questionnaire accurately:")
        st.write("- **Photo ID** (Driver's license, state ID, or passport) for you and your spouse.")
        st.write("- **Social Security Card** or ITIN documentation for yourself, your spouse, and dependents")
        st.warning("⚠️ Physical **social security cards** and **identification cards** must be present.")
        st.warning("⚠️ The **only exception** to not having phyiscal cards is if you have been at **this** VITA site in previous years.")
        st.write("- **Income Documents** (W-2s, 1099s, unemployment forms, etc.)")
        st.write("- **Deduction & Credit Documentation** (receipts for charitable donations, education expenses, medical expenses, child care expenses, etc.)")
        st.write("- **Health Insurance Information** (Form 1095-A, 1095-B, or 1095-C)")
        st.write("- **Previous Year Tax Return** (optional, but helpful for reference)")
        st.write("- Having these documents ready will help you complete the questionnaire faster and ensure accurate reporting.")
        st.write("Note: There is an 'Upload' documents feature at the bottom of this questionnaire as well.")
        

def BasicInfo():
    global answers, pronouns, pronouns2
    # Dictionary to store answers
    # Collect user input
    #(answers, key_name, question, input_type="text", options=None, columns=True)
    # Single-selection Filing Status
    current_tax_year=date.today().year-1
    with st.expander("Basic Information ", expanded=False):
        ask_question(answers, "tax_year",
            "Select the Tax Year:",
            input_type="radio",
            options=list(range(current_tax_year, current_tax_year - 5, -1)),
            index=0,use_index=True
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
        if answers.get('filing_status') == "Married Filing Jointly":
            pronouns='you or your spouse'
            Pronouns='you or your spouse'
            pronouns2="your or your spouse's"
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
                        st.warning("✅ Your filing status is married filing jointly.")
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
                st.warning("✅ Your filing status is qualifying surviving spouse.")
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
            f"Did {pronouns} have health insurance for any member of {pronouns2} household?",
            input_type="radio",
            options=health_insurance_responses,
            columns=False,  # important
            help_text=f"Household includes {pronouns} and anyone {pronouns} claim as a dependent on {pronouns2} tax return."
        )
        if answers.get("insurance_status") in health_insurance_responses[0:2]:
            ask_question(answers, "health_forms", f"Which form(s) do {pronouns} have?", 
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
                            f"The 1095-A lists someone not on {pronouns} tax return",
                            "A person on this tax return was enrolled in another taxpyers Marketplace coverage. (The person is listed on a Form 1095-A sent to a taxpayer not on this tax return.)",
                            f"You got married during {answers.get('tax_year')}, were unmarried as of January 1st, {answers.get('tax_year')}, and want to do an alternative calculation for year of marriage.",
                            f"{Pronouns} are self employed and want to deduct their health insurance premiums."]
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
            f"Last year, did {pronouns} rent in California for at least 6 months or more?",
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
            f"Which of the following best describes {pronouns2} living situation last year?",
            input_type="radio",
            options=ca_residency,
            columns=False
        )
        if answers.get("ca_residency") ==  ca_residency[2]:
           st.warning(f"⚠️ {Pronouns} may be required to fill out another state return of which, this site will not be able to assist {pronouns} in filing state taxes other than California.")

def MiscQuestions():
    global answers
    global typical_basic_response
    with st.expander("Miscallenous Questions", expanded=False):        
        ask_question(
            answers,
            "IHSS",
            f"Are {pronouns} an In Home Supportive Services (IHSS) provider?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )
        if answers.get("IHSS") ==  "Yes":
            ask_question(
                answers,
                "IHSS_live_with_anyone",
                f"For IHSS, did {pronouns} live with anyone {pronouns} took care of?",
                input_type="radio",
                options=typical_basic_response,
                columns=False
            )
        ask_question(
            answers,
            "IPPIN",
            f"Do {pronouns} have an IRS issued IPPIN?",
            input_type="radio",
            options=typical_basic_response,
            columns=False,
            help_text=f"An IPPIN is a six-digit number the IRS issues to taxpayers to help prevent someone else from filing a fraudulent tax return using {pronouns} Social Security number."
        )
        answers["EstimatedTaxPayments"] = []
        ask_question(
            answers,
            "EstimatedTaxPayments",
            f"Did {pronouns} make any estimated tax payments throughout {answers.get('tax_year')}?",
            input_type="radio",
            options=typical_basic_response,
            columns=False,
            help_text=f"Estimated tax payments are periodic payments {pronouns} make to the government during the year on income that isn’t automatically taxed through withholding, such as self employment."
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
    global answers, typical_basic_response, pronouns
    st.warning("🔵 Rental income is out of scope.")
 #   st.write("This section screens for uncommon, out-of-scope scenarios and helps prepare for the intake interview.")
#    st.write("Common items like W-2s, dividends, and interest are generally in scope.")
    #with st.expander("Wages, Dividends, Interest, Gambling Winnings, Certain Government Benefits, and Cancellation of Debt \n\n W-2, 1099-Div, 1099-Int, W-2G, 1099-G, 1099-C ", expanded=False):
    with st.expander("Wages, Dividends, Interest: W-2, 1099-Div, 1099-Int ", expanded=False):
        ask_question(
            answers,
            "W-2s",
            f"Do {pronouns} have any W-2s?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("W-2s") == "Yes":
            ask_question(
                answers,
                "Number_of_W-2",
                f"How many W-2s do {pronouns} have?",
                input_type="number",step=1
            )
        ask_question(
            answers,
            "1099-Div",
            f"Do {pronouns} have dividend income?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("1099-Div") == "Yes":
            ask_question(
                answers,
                "Number_of_1099-Div",
                f"How many 1099-Div Forms do {pronouns} have?",
                input_type="number",step=1
            )
        ask_question(
            answers,
            "1099-Int",
            f"Do {pronouns} have any interest income?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("1099-Int") == "Yes":
            ask_question(
                answers,
                "Number_of_1099-Int",
                f"How many 1099-Int forms do {pronouns} have?",
                input_type="number",step=1
            )
    with st.expander("Gambling Winnings, Certain Government Benefits, and Cancellation of Debt: W-2G, 1099-G, 1099-C ", expanded=False):
        ask_question(
            answers,
            "W-2G",
            f"Do {(pronouns)} have any gambling winnnings?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("W-2G") == "Yes":
            ask_question(
                answers,
                "Number_of_W-2G",
                f"How many W-2G Ffrms do {pronouns} have?",
                input_type="number",step=1
            )
        ask_question(
            answers,
            "1099-G_Refunds",
            f"Do {(pronouns)} have any refund of state or local income taxes?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("1099-G_Refunds") == "Yes":
            ask_question(
                answers,
                "Number_of_1099-G_Refunds",
                f"How many 1099-G forms with state or local income taxes do {pronouns} have? ",
                input_type="number",step=1
            )
        ask_question(
            answers,
            "1099-G_Benefits",
            f"Do {(pronouns)} have any payments from unemployment or paid family leave?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("1099-G_Benefits") == "Yes":
            ask_question(
                answers,
                "Number_of_1099-G_Benefitss",
                f"How many 1099-G forms with unemployment benefits or paid family leave do {pronouns} have? ",
                input_type="number",step=1
            )
        ask_question(
            answers,
            "1099-C",
            f"Do {(pronouns)} have cancellation of debt (1099-C)?",
            input_type="radio",
            options=typical_basic_response,
            columns=False
        )  
        if answers.get("1099-C") == "Yes":
            ask_question(
                answers,
                "Screening_1099-C",
                f"Do all the following apply? \n\n• Cancellation of debt included cancellation of debt included nonbusiness credit card debt cancellation including interest in box 3 when {pronouns} are solvent before the cancellation \n\n• Discharge of qualified principal residence indebtedness \n\n• Cancellation of debt included discharge of certain student loan debt in 2021 through 2025 \n\n \n\n• Cancellation of debt does not include an amount for interest ",
                    input_type="radio",
                    options=typical_basic_response
                    )
        if answers.get("Screening_1099-C") == "Yes":
            st.warning("❌ Out of Scope")
        if answers.get("Screening_1099-C") == "No":
                    ask_question(
                        answers,
                        "Number_of_1099-C",
                f"How many 1099-C forms do {pronouns} have? ",
                input_type="number",step=1
                            )


def F1099R():
    global answers, typical_basic_response, pronouns
    with st.expander("Distributions: 1099-R", expanded=False):        
        ask_question(
            answers,
            "1099-R",
            f"Do {pronouns} have distributions from a retirment account? (1099-R)",
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
                f"Do all {pronouns2} 1099-R forms have code 7 in box 7 AND the IRA/SEP/SIMPLE box is NOT checked?",
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
                    f"Do any of {pronouns2} 1099-R forms involve a traditional IRA to ROTH IRA conversion?",
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
                        f"Do any of {pronouns2} 1099-R forms have code 1 in box 7?",
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
                    if answers.get("code_1") == "No" or answers.get("code_1") == "Yes":
                        ask_question(
                            answers,
                            "bad_codes",
                            f"Do any of {pronouns2} 1099-R forms have any of these codes in box 7: 5, 8, 9, A, E, J, K, N, P, R, T, U?",
                            input_type="radio",
                            options=typical_basic_response,
                            columns=False
                        )
                        if answers.get("bad_codes") == "Yes":
                            st.warning("❌ Out of Scope")
                            return
                        ask_question(
                            answers,
                            "code_2_or_7_ira_nondeduct",
                            f"Do any of {pronouns2} 1099-R formsr have code 2 or 7 in box 7 AND IRA/SEP/SIMPLE box checked AND {pronouns} made nondeductible contributions?",
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
                            f"Do any of {pronouns2} 1099-R forms have code 2 in box 7?",
                            input_type="radio",
                            options=typical_basic_response,
                            columns=False
                        )
                        if answers.get("code_2") == "Yes":
                            ask_question(
                                answers,
                                "code_2_ira_nondeduct",
                                f"Is IRA/SEP/SIMPLE checked AND did {pronouns} make nondeductible contributions?",
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
                        ask_question(
                            answers,
                            "code_4",
                            f"Do any of {pronouns2} 1099-R forms have code 4 in box 7?",
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
    global pronouns, pronouns2
    with st.expander("Social Security: SSA-1099", expanded=False):        
        global answers, yes_no
        # Step 1: Do they have SSA at all?
        ask_question(
            answers,
            "has_ssa",
            f"Did {pronouns} receive any Social Security benefits (SSA-1099)?",
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
            f"Does {pronouns2} Social Security form include payments for prior years (lump-sum payments)?",
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
    f"⚠️ {pronouns} must enter details for each prior-year Social Security lump-sum payment as reported on previous tax returns (Form 1040)."
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
                min_value=0,
                step=100,
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
        st.success("✅ Lump sum Social Security details captured")

def OtherIncome():
    global answers, yes_no, pronouns, pronouns2
    with st.expander("Other Income", expanded=False):
        ask_question(
            answers,
            "other_income",
            f"Do {pronouns} have any any other income?",
            input_type="radio",
            options=yes_no,
            columns=False
        )
        if answers.get("other_income") == "Yes":
            answers["other_income_explaination"] = st.text_area(
                "Please briefly explain other income:",
                key="other_income_explaination"
            )

    
def SchC():
    global answers, yes_no, pronouns, pronouns2
    standard_mileage_rates = {
        2021: 0.56,
        2022: 0.585,
        2023: 0.655,
        2024: 0.67,
        2025: 0.70,
        2026: 0.725
    }
    tax_year = int(answers.get("tax_year"))
    standard_mileage_rate = standard_mileage_rates.get(tax_year)
    with st.expander("Self Employment: Schedule C", expanded=False):
        ask_question(
            answers,
            "has_self_employent",
            f"Do {pronouns} have any 1099-Ks, 1099-MISCs, 1099-NECs, or cash income associated with self employment?",
            input_type="radio",
            options=yes_no,
            columns=False
        )
        if answers.get("has_self_employent") != "Yes":
            return
        st.warning("⚠️ Businesses with asset purchases over $2,500 or net losses are out of scope.")
        st.warning(f"⚠️ You not enter actual car expenses such as gas, tires, and maintanance, you may, however take the standard mileage rate at ${standard_mileage_rate:.2f} per mile.")
        
        num_years = st.number_input(
            "How many self-employment businesses?",
            min_value=1,
            max_value=5,
            step=1
        )

        # ALWAYS reset cleanly
        answers["schedule_c_details"] = []

        for i in range(int(num_years)):
            ind=i+1
            st.markdown(f"### 💼 Business #{i+1}")

            year_data = {}

            # ---------------- BASIC INFO ----------------
            year_data["business_type"] = st.radio(
                "Business Description",
                ["Taxi & limousine service (Uber / Lyft)", "Other"],
                index=None,
                key=f"business_type_{i}"
            )

            if year_data["business_type"] == "Other":
                year_data["other_business"] = st.text_input(
                    f"Describe {pronouns2} business:",
                    key=f"SCH_C_other_business_{i}"
                )

            year_data["1099_nec_amounts"] = st.number_input("Number of 1099-NEC Forms", min_value=0, step=1, key=f"nec_{i}")
            year_data["1099_k_amounts"] = st.number_input("Number of 1099-K Forms", min_value=0, step=1, key=f"k_{i}")
            year_data["1099_misc_amounts"] = st.number_input("Number of 1099-MISC Forms", min_value=0, step=1, key=f"misc_{i}")
            year_data["other_cash_income"] = st.number_input("Other Cash Income ($)", step=50, key=f"cash_{i}")

            # ---------------- EXPENSES ----------------
            st.subheader("Business Expenses")

            year_data["advertising"] = st.number_input("Advertising ($)", step=50, key=f"adv_{i}")
            year_data["contract_labor"] = "Out of Scope"
            year_data["commission_and_fees"] = st.number_input("Commission ($)", step=50, key=f"comm_{i}")
            year_data["depletion"] = "Out of Scope"
            year_data["employee_benefits_programs"] = "Out of Scope"
            year_data["health_insurance"] = st.number_input("Health Insurance ($)", step=50, key=f"hi_{i}")
            year_data["insurance_other_than_health"] = st.number_input("Insurance ($)", step=50, key=f"ins_{i}")
            year_data["mortgage_interest"] = "Out of Scope"
            year_data["other_interest"] = st.number_input("Insurance ($)", step=50, key=f"other_interest_{i}")            
            year_data["legal_and_professional_services"] = st.number_input("Legal expenses($)", step=50, key=f"legal_{i}")
            year_data["office_expenses"] = st.number_input("Office expeneses ($)", step=50, key=f"office_{i}")
            year_data["pension_and_profit_sharing"] = "Out of Scope"
            year_data["rent_or_lease"] = st.number_input("Rent or Lease of Property or Equipement ($)", step=50, key=f"equip_{i}")
            #year_data["b_property"] = st.number_input("Property Rent", step=50, key=f"rent_{i}")
            year_data["repairs_and_maintenance"] = st.number_input("Repairs ($)", step=50, key=f"rep_{i}")
            year_data["supplies"] = st.number_input("Supplies ($)", step=50, key=f"supp_{i}")
            year_data["taxes_and_licenses"] = st.number_input("Taxes & Licenses ($)", step=50, key=f"tax_{i}")
            year_data["travel"] = st.number_input("Travel ($)", step=50, key=f"travel_{i}")
            year_data["meals_and_entertainment"] = "Out of Scope"
            year_data["utilities"] = st.number_input("Utilities ($)" , step=50, key=f"util_{i}")
            year_data["wages"] = st.number_input("Wages ($)", step=50, key=f"wages_{i}")
            year_data["other_expenses"] = st.number_input("Other Expenses ($)", step=50, key=f"other_expenses_{i}")
            if year_data["other_expenses"] > 0:
                year_data["other_expenses_explaination"] = st.text_input(
                    "Please explain Other Expenses:",
                    key=f"other_expenses_explaination_{i}"
                )
            # ---------------- VEHICLE ----------------
            st.subheader("Car and Truck Expenses")

            year_data["SCH_C_vehicle_desc"] = st.text_input(
                "Vehicle Description",
                key=f"desc_{i}"
            )
            year_data[f"SCH_C_vehicle_date"] = st.date_input(
                "Date Placed in Service",
                key=f"date_{i}"
            )
            year_data["buesiness_miles"] = st.number_input(
                "Business Miles",
                step=50,
                key=f"miles_{i}",
                help="Do not include commuting mileage."
            )
            year_data[f"SCH_C_vehicle_other"] = st.radio(
                "Other vehicle available?",
                options=yes_no,
                index=None,
                key=f"other_veh_available_{i}"
            )

            year_data[f"SCH_C_vehicle_off_duty"] = st.radio(
                "Available off duty?",
                options=yes_no,
                index=None,
                key=f"off_duty_{i}"
            )

            year_data[f"SCH_C_vehicle_evidence"] = st.radio(
                "Evidence available?",
                options=yes_no,
                index=None,
                key=f"evidence_{i}"
            )

            # ✅ APPEND INSIDE LOOP (FIXED)
            answers["schedule_c_details"].append(year_data)


def SchD():
    global answers, yes_no, typical_basic_response, pronouns, pronouns2
    with st.expander("Sale of Capital Assets: Schedule D", expanded=False):
        ask_question(
            answers,
            key_name="sold_stocks_or_etfs",
            question=f"Did {pronouns} sell stocks, mutual funds, or ETFs outside a retirement account?",
            input_type="radio",
            options=typical_basic_response
        )
        ask_question(
            answers,
            key_name="transactions",
            question=f"Did {pronouns} have transactions involving options, futures, or commodities?",
            input_type="radio",
            options=typical_basic_response
        )
        if answers.get('transactions') == "Yes":
            st.warning("❌ Out of scope.")
            return
        ask_question(
            answers,
            key_name="crypto",
            question=f"Did {pronouns} sell any cyptocurrency assets or earn any cryptocurrency income (1099-DA)?",
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
            question=f"Do any of these codes appear on {pronouns2} 1099-B forms? \n\n C, D, N, Q, R, S, X, Y, or Z",
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
            question=f"Do {pronouns} have complex basis adjustments such as cnoncovered securities, unreported cost basis or wash sales (unless wash sale adjustment is reported clearly)?",
            input_type="radio",
            options=typical_basic_response
            )
        if answers.get('complex_basis') == "Yes":
                st.warning("❌ Out of scope.")
                return


def Deductions():
    global answers, yes_no, typical_basic_response
    if answers.get('tax_year')>=2025:
        with st.expander("No Tax on Tip", expanded=False):
            ask_question(
                    answers,
                    key_name="no_tax_on_tip",
                    question=f"Did {pronouns} have tips not reported on W-2s or 1099-s?",
                    input_type="radio",
                    options=typical_basic_response,
                    help_text="W-2 box 7 is tips and may be tax deductible."
                )
            if answers.get('no_tax_on_tip') == "Yes":
                answers["no_tax_on_tip_amount"] = st.number_input(
                    f"How much did {pronouns} receive in tips not already reported? ($)",
                    min_value=0,
                    step=100,
                    key="no_tax_on_tip_amount"
                )
        with st.expander("No Tax on Overtime", expanded=False):
            ask_question(
                    answers,
                    key_name="no_tax_on_overtime",
                    question=f"Did {pronouns} have overtime not reported on your W-2s?",
                    input_type="radio",
                    options=typical_basic_response,
                    help_text="Typically 'OT' or similiar in box 14."
                )
            if answers.get('no_tax_on_overtime') == "Yes":
                answers["no_tax_on_overtime_amount"] = st.number_input(
                    f"How much did {pronouns} receive in overtime not already reported? ($)",
                    min_value=0,
                    step=100,
                    key="no_tax_on_overtime_amount"
                )
        with st.expander("Car Loan Interest (1098-VLI)", expanded=False):
            ask_question(
                    answers,
                    key_name="no_tax_on_car_interest",
                    question=f"Did {pronouns} have qualified car loan interest?",
                    input_type="radio",
                    options=typical_basic_response
                )
            if answers.get('no_tax_on_car_interest') == "Yes":
                answers["no_tax_on_car_interest_amount"] = st.number_input(
                    f"How much did {pronouns} pay in qualified car loan interest? ($)",
                    min_value=0,
                    step=100,
                    key="no_tax_on_car_interest_amount"
                )

    with st.expander("Student Loan Interest: 1098-E", expanded=False):
        ask_question(
            answers,
            key_name="student_loan_interest",
            question=f"Did {pronouns} pay any student loan interest?",
            input_type="radio",
            options=typical_basic_response
        )
        if answers.get('student_loan_interest') == "Yes":
             st.warning(f"✅ In scope, lease have {pronouns2} 1098-E forms handy.")
    with st.expander("Qualified Educator", expanded=False):
        ask_question(
                answers,
                key_name="qualified_educator",
                question=f"Are {pronouns} a K-12 teacher, instructor, counselor, aide, or principal who worked at least 900 hours during the school year?",
                input_type="radio",
                options=typical_basic_response
            )
        if answers.get('qualified_educator') == "Yes":
             answers["ssa_received"] = st.number_input(
                f"How much did {pronouns} spend on out of pocket clasroom expenses? ($)",
                min_value=0,
                step=100,
                key="educator_amount"
            )
    with st.expander("Health Saving Account (HSA) Contribution Deduction", expanded=False):
        ask_question(
                answers,
                key_name="HSA_Deduction",
                question=f"Did {pronouns} contribute to a HSA?",
                input_type="radio",
                options=typical_basic_response
            )
        if answers.get('HSA_Deduction') == "Yes":
             answers["HSA_Deduction_Amount"] = st.number_input(
                f"How much did {pronouns} contribute to a HSA. ($)",
                min_value=0,
                step=100,
                key="HSA_Deduction_Amount"
            )
    with st.expander("Traditional Individual Retirement Account (IRA) Deduction", expanded=False):
        ask_question(
                answers,
                key_name="IRA_Deduction",
                question=f"Did {pronouns} contribute to a traditional IRA?",
                input_type="radio",
                options=typical_basic_response
            )
        if answers.get('IRA_Deduction') == "Yes":
             answers["IRA_Deduction_Amount"] = st.number_input(
                f"How much did {pronouns} contribute to traditional IRA. ($)",
                min_value=0,
                step=100,
                key="IRA_Deduction_Amount"
            )
    with st.expander("Itemized Deductions", expanded=False):
        ask_question(
                answers,
                key_name="cash_gifts",
                question=f"Did {pronouns} have any cash gifts to charity?",
                input_type="radio",
                options=yes_no
            )
        st.write(answers.get('cash_gifts')=="Yes")
        if answers.get('cash_gifts') == "Yes":
            ask_question(
                answers,
                key_name="cash_gift_amounts",
                question=f"How much did {pronouns} give to charity in cash? ($)",
                input_type="number",
                options=typical_basic_response
            )
        ask_question(
                answers,
                key_name="itemize_question",
                question=f"Did {pronouns} want to take an itemized deduction?",
                input_type="radio",
                options=typical_basic_response,
                help_text="Most taxpayers take their standard deduction (> $15,000) and do not itetmize as only certain expeses qualify. \n\n Qualified expenses includes: \n\n mortgage interest, unreimbursed medical expenses, gifts to charity. real estate, local, and state taxes paid."
            )
        filings_statuses2 = ["Single", "Head of Houeshold", "Married Filing Jointly", "Married Filing Separately","Qualified Surviving Spouse"]
        sch_a_expensess=["Mortgage Interest","Real Estate Taxes","Cash Gifts to Charity","Non-Cash Gifts to Charity","DMV Tags","Medical Expenses","Gambling Losses","Other"]
        st.write(answers.get('itemize_question')=="Yes")
        if answers.get('itemize_question') == "Yes":
            ask_question(
                answers,
                key_name="last_years_filing_status",
                question=f"What was {pronouns2} filing status last tax year?",
                input_type="radio",
                options=filings_statuses2,columns=False
            )
            ask_question(
                answers,
                key_name="itemized_expenses",
                question=f"Which of the following expensesdo {pronouns2} have?",
                input_type="checkbox",
                options=sch_a_expensess,
                columns=False
            )
            st.warning("⚠️ Please have forms and documentation handy.")
        selected = answers.get("itemized_expenses", [])
        if "Mortgage Interest" in selected:
            ask_question(
                answers,
                key_name="mortgage_interest",
                question=f"Mortgage interest ($)",
                input_type="number",step=50
            )
        if "Mortgage Interest" in selected:
            ask_question(
                answers,
                key_name="sch_a_mortgage_interest",
                question="Mortgage interest ($)",
                input_type="number",
                step=50
            )

        if "Real Estate Taxes" in selected:
            ask_question(
                answers,
                key_name="sch_a_real_estate_taxes",
                question="Real estate taxes ($)",
                input_type="number",
                step=50
            )

        if "Cash Gifts to Charity" in selected:
            ask_question(
                answers,
                key_name="sch_a_cash_gifts_to_charity",
                question="Cash gifts to charity ($)",
                input_type="number",
                step=50
            )

        if "Non-Cash Gifts to Charity" in selected:
            ask_question(
                answers,
                key_name="sch_a_non_cash_gifts_to_charity",
                question="Non-cash gifts to charity ($)",
                input_type="number",
                step=50
            )

        if "DMV Tags" in selected:
            ask_question(
                answers,
                key_name="sch_a_dmv_tags",
                question="DMV tags/registration ($)",
                input_type="number",
                step=50
            )

        if "Medical Expenses" in selected:
            ask_question(
                answers,
                key_name="sch_a_medical_expenses",
                question="Medical expenses ($)",
                input_type="number",
                step=50
            )

        if "Gambling Losses" in selected:
            ask_question(
                answers,
                key_name="sch_a_ambling_losses",
                question="Gambling losses ($)",
                input_type="number",
                step=50
            )

        if "Other" in selected:
            ask_question(
                answers,
                key_name="sch_a_other_expenses",
                question="Other expenses ($)",
                input_type="number",
                step=50
            )
            if answers["sch_a_other_expenses"] > 0:
                answers["sch_a_other_expenses_explanation"] = st.text_input(
                    "Please explain other expenses:",
                    key=f"sch_a_other_expenses_explanation"
                )






















































def CDCC():
    global answers, yes_no, pronouns, pronouns2

    with st.expander("Child & Dependent Care Credit (CDCC)", expanded=False):

        ask_question(answers, "child_care_expenses",
            f"Do {pronouns2} have child care expenses for children under 13?",
            input_type="radio",
            options=yes_no
        )  
        if answers.get('child_care_expenses') == 'Yes':

            # =========================
            # BACKGROUND (GLOBAL ONCE)
            # =========================
            st.subheader("Background Information")

            cdcc_background = {}

            cdcc_background["tax_zero"] = st.radio(
                "Is your taxable income or tax liability $0?",
                options=yes_no,
                index=None,
                key="CDCC_tax_zero"
            )

            cdcc_background["employer_benefits"] = st.radio(
                "Did you receive dependent care benefits not on W-2?",
                options=yes_no,
                index=None,
                key="CDCC_employer_benefits"
            )

            cdcc_background["disability_student"] = st.radio(
                f"Were {pronouns} unable to work due to disability or school?",
                options=yes_no,
                index=None,
                key="CDCC_disability_student"
            )

            if cdcc_background["disability_student"] == "Yes":
                cdcc_background["months_you"] = st.number_input(
                    "Months YOU unable to work",
                    min_value=0,
                    max_value=12,
                    step=1,
                    key="CDCC_months_you"
                )

                if answers.get("filing_status") == "Married Filing Jointly":
                    cdcc_background["months_spouse"] = st.number_input(
                        "Months SPOUSE unable to work",
                        min_value=0,
                        max_value=12,
                        step=1,
                        key="CDCC_months_spouse"
                    )

            # =========================
            # CHILD LOOP (LIKE SCHEDULE C BUSINESSES)
            # =========================
            st.subheader("Child Information")

            num_children = st.number_input(
                "How many qualifying children? (Max 5)",
                min_value=1,
                max_value=5,
                step=1,
                key="CDCC_num_children"
            )

            answers["CDCC_children"] = []

            tax_year = int(answers.get("tax_year"))
            ref_date = date(tax_year, 12, 31)

            for i in range(int(num_children)):
                st.markdown(f"### 👶 Child #{i+1}")

                child_data = {}

                # ---------------- CHILD INFO ----------------
                child_data["name"] = st.text_input(
                    "Child’s Name",
                    key=f"CDCC_child_name_{i}"
                )

                child_data["birthday"] = st.date_input(
                    "Child’s Birthday",
                    key=f"CDCC_child_birthday_{i}"
                )

                # AGE CALC
                if child_data["birthday"]:
                    child_data["age"] = (
                        ref_date.year
                        - child_data["birthday"].year
                        - ((ref_date.month, ref_date.day) <
                        (child_data["birthday"].month, child_data["birthday"].day))
                    )
                else:
                    child_data["age"] = None

                st.write(f"Age as of {tax_year}: **{child_data['age']}**")

                # =========================
                # PROVIDER INFO (INSIDE LOOP)
                # =========================
                child_data["provider_id_type"] = st.radio(
                    "Provider ID Type",
                    options=["EIN", "SSN"],
                    index=None,
                    key=f"CDCC_provider_id_type_{i}"
                )
                st.warning("Please have your provider's information handy.")

                child_data["provider_name"] = st.text_input(
                    "Provider Name",
                    key=f"CDCC_provider_name_{i}"
                )

                child_data["provider_address"] = st.text_area(
                    "Provider Address",
                    key=f"CDCC_provider_address_{i}"
                )

                child_data["provider_phone"] = st.text_input(
                    "Provider Phone",
                    key=f"CDCC_provider_phone_{i}"
                )

                child_data["provider_flags"] = []

                if st.checkbox("The provider is tax exempt", key=f"CDCC_flag_exempt_{i}"):
                    child_data["provider_flags"].append("Tax Exempt")

                if st.checkbox("The provider is my household employee", key=f"CDCC_flag_household_{i}"):
                    child_data["provider_flags"].append("Household Employee")

                if st.checkbox("I was living abroad and used a foreign provider", key=f"CDCC_flag_foreign_{i}"):
                    child_data["provider_flags"].append("Foreign Provider")

                child_data["amount_paid"] = st.number_input(
                    f"Amount Paid ({tax_year})",
                    min_value=0,
                    step=100,
                    key=f"CDCC_amount_paid_{i}"
                )

                # ---------------- APPEND LIKE SCHC ----------------
                answers["CDCC_children"].append(child_data)

            # =========================
            # STORE FINAL STRUCTURE
            # =========================
            answers["CDCC_details"] = {
                "background": cdcc_background,
                "children": answers["CDCC_children"]
            }










def EducationCredits():
    global answers, yes_no, pronouns2

    with st.expander("Education Credits (1098-T)", expanded=False):
        ask_question(answers, "educational_expenses",
            f"Do you, your spouse, or any of your dependents have any educational expenses?",
            input_type="radio",
            options=yes_no
        )  
        if answers.get('educational_expenses') == 'Yes':
            # =========================
            # STUDENT LOOP
            # =========================
            st.subheader("Student Information")

            num_students = st.number_input(
                "How many students? (Max 5)",
                min_value=1,
                max_value=5,
                step=1,
                key="EDU_num_students"
            )

            answers["EDU_students"] = []
            tax_year = int(answers.get("tax_year"))
            for i in range(int(num_students)):
                st.markdown(f"### 🎓 Student #{i+1}")
                student = {}
                student["name"] = st.text_input(
                    "Student Name",
                    key=f"EDU_name_{i}"
                )
                student["relationship"] = st.text_input(
                    "Relationship to You",
                    key=f"EDU_relationship_{i}",help="Examples: Self, Daughter, Son"
                )
                student["age"] = st.number_input(
                    f"Age of student as of December 31, {tax_year}",
                    min_value=18,
                    step=1,
                    key=f"EDU_age_{i}"
                )
                # ---------------- STATUS ----------------
                student["enrollment_status"] = st.radio(
                    "Student Status (Enrollment)",
                    ["Below Part Time", "Part Time", "Full Time"],
                    index=None,
                    key=f"EDU_enrollment_{i}"
                )
                student["level"] = st.radio(
                    "Student Level",
                    ["Graduate", "Undergraduate", "Neither"],
                    index=None,
                    key=f"EDU_level_{i}"
                )
                student["years_post_secondary"] = st.number_input(
                    f"How many years of Post-Secondary school has the student completed as of December 31, {tax_year}",
                    min_value=0,
                    step=1,
                    key=f"EDU_years_{i}"
                )
                student["felony_drug"] = st.radio(
                    "Does the student have a felony drug conviction?",
                    yes_no,
                    index=None,
                    key=f"EDU_felony_{i}"
                )
                student["aotc_4_years"] = st.radio(
                    "Has the student claimed AOTC for more than 4 years?",
                    yes_no,
                    index=None,
                    key=f"EDU_aotc_{i}"
                )
                student["box4_or_6"] = st.radio(
                    "Are there any amounts in Box 4 or Box 6?",
                    yes_no,
                    index=None,
                    key=f"EDU_box46_{i}"
                )
                if student.get('box4_or_6')=="Yes":
                    st.warning("❌ Out of scope")
                    return
                student["payments_box1"] = st.number_input(
                    "1) Payments Received (Box 1)  ($)",
                    min_value=0,
                    step=100,
                    key=f"EDU_box1_{i}"
                )
                student["scholarships_box5"] = st.number_input(
                    "2) Scholarships or Grants (Box 5)  ($)",
                    min_value=0,
                    step=100,
                    key=f"EDU_box5_{i}"
                )
                
                student["additional_expenses"] = st.number_input(
                    "3) Additional qualified expenses (books, supplies, etc.) ($)",
                    key=f"EDU_expenses_{i}",min_value=0
                )
                student["additional_qualified_expenses_amount"] = st.number_input(
                    "Total Additional Qualified Educational Expenses Amount  ($)",
                    min_value=0,
                    step=100,
                    key=f"EDU_expenses_amt_{i}",
                    help="Qualified educational expenses include tuition, fees, books and supplies required for school."
                )
                # ---------------- CALCULATION ----------------
                qee = (
                    student["payments_box1"]
                    + student["additional_qualified_expenses_amount"]
                    - student["scholarships_box5"]
                )
                student["qualified_expenses"] = qee
                st.write(f"### Calculated Qualified Expenses: **{qee}**")
                if qee > 0:
                    st.success("✅ Eligible qualified education expenses")
                elif qee < 0:
                    st.warning("Possible taxable scholarship income")
                else:
                    st.warning("No net qualified expenses")
                # ---------------- APPEND ----------------
                answers["EDU_students"].append(student)
            # =========================
            # FINAL STORAGE
            # =========================
            answers["EducationCredits"] = {
                "students": answers["EDU_students"]
            }

def RefundAndPayment():
    global answers
    with st.expander("Refund and Payment Method", expanded=False):
        ref=["I expected to owe","I expect to get a refund","I am unsure"]
        ask_question(answers, "irs_refund",
            f"Do {pronouns} expect to owe or get a refund from the IRS?",
            input_type="radio",
            options=ref
        )  
        ask_question(answers, "ca_refund",
            f"Do {pronouns} expect to owe or get a refund from California?",
            input_type="radio",
            options=ref
        )  
        ask_question(answers, "refund_method",
            f"If {pronouns} are due a refund, how do {pronouns} want to receive it?",
            input_type="radio",
            options=["Direct Deposit (Bank)","CFR Card"],
            help_text="A CFR Card is a prepaid debit card that is mailed to you."
        )
        if answers.get('refund_method') == 'CFR Card':
            st.warning("🔵 Please have your e-mail, phone number, and address ready for the volunteer.")
        ask_question(answers, "payment_method",
            f"If {pronouns} have a balance due, how do {pronouns} want to pay it?",
            input_type="radio",
            options=["Direct Debit (Bank)","Setup installment plan","Mail Payment","Unsure"]
        )  
        if answers.get('payment_method') == 'Direct Debit (Bank)' or  answers.get('refund_method') == "Direct Deposit (Bank)":
            st.warning("🔵 Please have bank information ready for the volunteer.")

def FinalDisclaimer():
    with st.expander("Final Disclaimer", expanded=False):
        st.write(f"⚠️ {Pronouns} are ultimately responsible for {pronouns} tax return.")
        st.write(f"VITA volunteers will prepare the return based on the information {pronouns} provide.")
        st.write("Please ensure all information provided is accurate and complete.")
        st.write(f"{Pronouns} are responsible for reviewing the completed return before signing and e-filing.")
        st.write("VITA volunteers cannot provide legal or tax advice beyond the scope of the program.")
        st.write("By submitting, you confirm that the information provided is true and complete to the best of your knowledge.")