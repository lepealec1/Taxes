import streamlit as st
from Function import ask_question

answers={}

def BasicInfo():
    global answers
    # Dictionary to store answers
    # Collect user input
    #(answers, key_name, question, input_type="text", options=None, columns=True)

    # Single-selection Filing Status
    filings_statuses = ["Single", "Head of Houeshold", "Married Filing Jointly", "Married Filing Seperately"]
    with st.expander("Basic Information ", expanded=True):
        ask_question(
            answers,
            "filing_status",
            "Select your filing status:",
            input_type="radio",
            options=filings_statuses,
            columns=False,
            allow_none=True,
            help_text="Select your filing status"
        )
        ask_question(answers, "name", "First Name", input_type="text")
        ask_question(answers, "email", "Email", input_type="text")
        ask_question(answers, "phone", "Phone Number", input_type="text")
    # Insurance status with radio buttons in columns

def HealthInsurance():
    global answers

    with st.expander("Health Insurance", expanded=True):
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
    with st.expander("Residency Questions", expanded=True):        
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
           st.write("We will not be able to assist you in filing state taxes other than California.")

def MiscQuestions():
    global answers
    global typical_basic_response
    with st.expander("Miscallenous Questions", expanded=True):        
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
                "Did you live with anyone you took care of?",
                input_type="radio",
                options=typical_basic_response,
                columns=False
            )
