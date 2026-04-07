import streamlit as st

def BasicInfo():
    # Dictionary to store answers
    answers = {}
    # Collect user input
    answers['name'] = st.text_input("First Name")
    answers['phone'] = st.text_input("Phone Number")
    answers['email'] = st.text_input("Email")
    answers['phone'] = st.text_input(" Number")

    st.title("Health Insurance Questionnaire")

    # Question 1: Did you have health insurance?
    answers['insurance_status'] = st.radio(
        "Did you have health insurance for any member of your household?",
        options=["All Year", "Part Year", "No", "Unsure"]
    )

    # Question 2: Which forms do you have? (only show if All Year or Part Year)
    if answers['insurance_status'] in ["All Year", "Part Year"]:
        st.write("Which health insurance form(s) do you have?")
        forms_options = ["1095-A", "1095-B", "1095-C"]
        cols = st.columns(len(forms_options))
        # Dictionary to store selected forms
        selected_ans = []
        st.write("Which type of health insurance do you have?")
        for col, form in zip(cols, forms_options):
            if col.checkbox(form, key=f"form_{form}"):
                selected_ans.append(form)
        selected_ans = ["Medi-Cal", "Medicaid", "Medicare", "Employee Sponsored", "Other"]
        cols = st.columns(len(selected_ans))
        
        selected_coverage = []
        for col, cov in zip(cols, selected_ans):
            if col.checkbox(cov, key=f"coverage_{cov}"):
                selected_coverage.append(cov)
        # Display the results
        st.subheader("Your Answers")
        st.write("Insurance status:", answers['insurance_status'])
        if answers['insurance_status'] in ["All Year", "Part Year"]:
            st.write("Forms:", forms)
            st.write("Coverage type:", coverage_type)

        answers['refund_method'] = st.selectbox("Refund Method", ["Direct Deposit", "Check by Mail"])
        
        return answers


