import streamlit as st

st.set_page_config(layout="wide")

st.title("Supplemental Questionnaire")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.text_input("Name")
with col2:
    st.date_input("Date")

st.divider()

# Helper to create a row
def grid_row(question, options=("Yes", "No", "Unsure")):
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(question)
    with col2:
        return st.radio(
            label="",
            options=options,
            horizontal=True,
            label_visibility="collapsed"
        )

# --- Health Insurance Row ---
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
**Did you have health insurance for any member of your household?**  
→ If all year or part year, which forms?  
→ If all year or part year, what type? Medi-Cal? Medicaid? Other?
""")
with col2:
    st.radio("", ["All Year", "Part Year", "No", "Unsure"], horizontal=True, label_visibility="collapsed")
    st.checkbox("1095-A")
    st.checkbox("1095-B")
    st.checkbox("1095-C")
    st.text_input("Answer", label_visibility="collapsed")

st.divider()

# --- Standard Rows ---
grid_row("Did you rent in California for more than 6 months of the year?")
grid_row("Are you an In Home Supportive Services (IHSS) provider?")
grid_row("Do you or your spouse have an IRS issued protection PIN (IPPIN)?")

# --- 1099-R Section ---
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
**Did you receive a 1099-R?**  
→ If yes, is it code 7 with IRA/SEP/SIMPLE not checked?  
→ If yes, is it code 1?  
→ If code 1, what did you use the early distributions on?
""")
with col2:
    st.radio("", ["Yes", "No", "Unsure"], horizontal=True, label_visibility="collapsed")
    st.radio("Code 7?", ["Yes", "No", "Unsure"], horizontal=True)
    st.radio("Code 1?", ["Yes", "No", "Unsure"], horizontal=True)
    st.text_input("Answer", label_visibility="collapsed")

st.divider()

grid_row("Did you get a Social Security lump sum for a prior year?")
grid_row("Do you have any income from self employment?")
grid_row("Do you have any above the line adjustments? (1098-E, 1098-VLI)")
grid_row("Did you sell any stocks not within a retirement account?")
grid_row("Do you want to take an itemized deduction?")
grid_row("Do you have child care expenses for children under 13?")
grid_row("Do you or dependents receive a 1098-T?")
grid_row("Did you make estimated tax payments?")

st.divider()

# --- Refund / Payment Grid ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("**If you have a refund due:**")
    st.radio("", ["Direct Deposit", "CFR Card", "Check by Mail"], label_visibility="collapsed")

with col2:
    st.markdown("**If you have a balance due:**")
    st.radio("", [
        "Direct Debit",
        "Installment Plan",
        "Mail Payment",
        "Direct Payment",
        "Unsure"
    ], label_visibility="collapsed")

st.divider()

# --- Bank Info ---
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("**Bank Name**")
with col2:
    st.text_input("", label_visibility="collapsed")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("**Type**")
with col2:
    st.radio("", ["Checking", "Saving"], horizontal=True, label_visibility="collapsed")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("**Routing Number**")
with col2:
    st.text_input("", label_visibility="collapsed")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("**Account Number**")
with col2:
    st.text_input("", label_visibility="collapsed")