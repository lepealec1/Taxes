from fpdf import FPDF
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Supplemental Questionnaire")

# Dictionary to store all answers
answers = {}

# --- Helper Functions ---

def grid_row(key, question, options=("Yes", "No", "Unsure")):
    """Create a question row with radio buttons and store answer."""
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(question)
    with col2:
        answers[key] = st.radio(
            question,  # descriptive label for accessibility
            options=options,
            horizontal=True,
            label_visibility="collapsed"
        )

def labeled_input(key, label, input_type="text", options=None):
    """Create a labeled input and store answer."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**{label}**")
    with col2:
        if input_type == "text":
            answers[key] = st.text_input(label, label_visibility="collapsed")
        elif input_type == "radio":
            answers[key] = st.radio(label, options, horizontal=True, label_visibility="collapsed")
        elif input_type == "checkbox":
            answers[key] = st.checkbox(label)
        return answers[key]

# --- Header ---
col1, col2 = st.columns([3, 1])
with col1:
    answers["name"] = st.text_input("Name", label_visibility="visible")
with col2:
    answers["date"] = st.date_input("Date", label_visibility="visible")

st.divider()

# --- Health Insurance Section ---
with st.expander("Health Insurance"):
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
**Did you have health insurance for any member of your household?**  
→ If all year or part year, which forms?  
→ If all year or part year, what type? Medi-Cal? Medicaid? Other?
""")
    with col2:
        answers["health_status"] = st.radio(
            "Health insurance status",
            ["All Year", "Part Year", "No", "Unsure"],
            horizontal=True,
            label_visibility="collapsed"
        )
        answers["1095_a"] = st.checkbox("1095-A")
        answers["1095_b"] = st.checkbox("1095-B")
        answers["1095_c"] = st.checkbox("1095-C")
        answers["health_note"] = st.text_input("Health insurance note", label_visibility="collapsed")

st.divider()

# --- Standard Questions ---
grid_row("rent_ca_6_months", "Did you rent in California for more than 6 months of the year?")
grid_row("ihss_provider", "Are you an In Home Supportive Services (IHSS) provider?")
grid_row("ippin", "Do you or your spouse have an IRS issued protection PIN (IPPIN)?")

# --- 1099-R Section ---
with st.expander("1099-R Information"):
    answers["received_1099r"] = st.radio(
        "Did you receive a 1099-R?", ["Yes", "No", "Unsure"], horizontal=True, label_visibility="collapsed"
    )
    answers["code7"] = st.radio(
        "Is it code 7 with IRA/SEP/SIMPLE not checked?", ["Yes", "No", "Unsure"], horizontal=True, label_visibility="collapsed"
    )
    answers["code1"] = st.radio(
        "Is it code 1?", ["Yes", "No", "Unsure"], horizontal=True, label_visibility="collapsed"
    )
    answers["early_dist_use"] = st.text_input(
        "If code 1, what did you use the early distributions on?", label_visibility="collapsed"
    )

st.divider()

# --- Additional Questions ---
grid_row("ss_lump_sum", "Did you get a Social Security lump sum for a prior year?")
grid_row("self_employment", "Do you have any income from self employment?")
grid_row("above_line_adj", "Do you have any above the line adjustments? (1098-E, 1098-VLI)")
grid_row("sold_stocks", "Did you sell any stocks not within a retirement account?")
grid_row("itemized_deduction", "Do you want to take an itemized deduction?")
grid_row("child_care_exp", "Do you have child care expenses for children under 13?")
grid_row("form_1098t", "Do you or dependents receive a 1098-T?")
grid_row("estimated_tax", "Did you make estimated tax payments?")

st.divider()

# --- Refund / Payment ---
with st.expander("Refund / Payment"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**If you have a refund due:**")
        answers["refund_method"] = st.radio(
            "Refund method",
            ["Direct Deposit", "CFR Card", "Check by Mail"],
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("**If you have a balance due:**")
        answers["balance_method"] = st.radio(
            "Balance payment method",
            ["Direct Debit", "Installment Plan", "Mail Payment", "Direct Payment", "Unsure"],
            label_visibility="collapsed"
        )

st.divider()

# --- Bank Info ---
with st.expander("Bank Information"):
    labeled_input("bank_name", "Bank Name")
    labeled_input("account_type", "Account Type", "radio", ["Checking", "Saving"])
    labeled_input("routing_number", "Routing Number")
    labeled_input("account_number", "Account Number")

st.divider()

# --- Show / Save Answers ---
st.subheader("Collected Answers")
st.json(answers)

# Optional: Button to download answers as CSV
if st.button("Download Answers as CSV"):
    df = pd.DataFrame([answers])
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "questionnaire_answers.csv", "text/csv")


def generate_pdf(answers_dict, filename="questionnaire.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", '', 12)
    for key, value in answers_dict.items():
        # Format lists nicely if any
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        pdf.multi_cell(0, 8, f"{key.replace('_',' ').title()}: {value}")
        pdf.ln(1)

    pdf.output(filename)
    return filename

if st.button("Download Answers as PDF"):
    pdf_file = generate_pdf(answers)
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name="questionnaire_answers.pdf",
            mime="application/pdf"
        )