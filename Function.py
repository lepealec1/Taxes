import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import datetime
import textwrap
import streamlit as st
import os
import pickle
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders





def safe_one_line(value, max_len=120):
    """Force everything into a single safe row"""
    if isinstance(value, datetime.date):
        value = value.strftime("%Y-%m-%d")

    text = str(value)

    # HARD truncate (prevents FPDF crash)
    if len(text) > max_len:
        text = text[:max_len] + "..."

    return text



import streamlit as st
def ask_question(answers, key_name, question,index=0, input_type="text", options=None, columns=True, help_text=None, allow_none=False):
    if input_type in ["text", "text_input"]:
        answers[key_name] = st.text_input(question, key=key_name, help=help_text)

    elif input_type == "radio":
        # Use session state to allow no initial selection
        if key_name not in st.session_state:
            st.session_state[key_name] = None  # start unselected

        selected = st.radio(
            question,
            options,
            index=index if not allow_none else None,  # None prevents auto-selection
            key=key_name,
            help=help_text
        )
        answers[key_name] = selected

    elif input_type == "checkbox":
        st.write(question)
        if help_text:
            st.caption(help_text)

        selected = []
        cols_list = st.columns(len(options)) if columns else [st]
        for col, option in zip(cols_list, options):
            if col.checkbox(option, key=f"{key_name}_{option}"):
                selected.append(option)
        answers[key_name] = selected

    return answers[key_name]

import streamlit as st

def ask_question(
    answers,
    key_name,
    question,
    input_type="text",
    index=0,
    use_index=False,
    options=None,
    columns=True,
    help_text=None,
    allow_none=False,
    multiple=False,
    min_value=0,
    step=0
):
    """
    Generic helper to ask a question in Streamlit and store in `answers` dict.
    Parameters:
        answers (dict): dictionary to store results
        key_name (str): key to store the answer
        question (str): question text
        input_type (str): "text", "number", "radio", "checkbox", "date"
        options (list): list of options (for radio/checkbox)
        columns (bool): if radio/checkbox, display horizontally
        help_text (str): optional help text
        allow_none (bool): allow None selection for radio
        multiple (bool): allow multiple entries for text/number (line-separated)
    """
    
    if input_type in ["text", "text_input"]:
        if multiple:
            # Use a text area for multiple entries (one per line)
            values = st.text_area(f"{question} (one per line)", key=key_name, help=help_text)
            answers[key_name] = [v.strip() for v in values.split("\n") if v.strip()]
        else:
            answers[key_name] = st.text_input(question, key=key_name, help=help_text)

    elif input_type == "number":
        if multiple:
            # Text area for multiple numbers (one per line)
            values = st.text_area(f"{question} (one per line)", key=key_name, help=help_text)
            cleaned = []
            for v in values.split("\n"):
                v = v.strip()
                if v:
                    try:
                        cleaned.append(float(v))
                    except ValueError:
                        st.warning(f"Invalid number skipped: {v}")
            answers[key_name] = cleaned
        else:
            answers[key_name] = st.number_input(question, key=key_name, min_value=min_value, step=step, help=help_text)

    elif input_type == "radio":
        # Ensure session state exists
        if key_name not in st.session_state:
            st.session_state[key_name] = None  # start unselected

        radio_options = options
        if allow_none:
            radio_options = ["None"] + (options or [])

        if use_index:
            if key_name not in st.session_state or st.session_state[key_name] not in radio_options:
                if allow_none:
                    st.session_state[key_name] = "None"
                else:
                    st.session_state[key_name] = radio_options[index] if radio_options else None
            selected = st.radio(
            question,
            options=radio_options,
            key=key_name,
            help=help_text,
            horizontal=columns)
        else:
            selected = st.radio(
                question,
                options=radio_options,
                index=index if not allow_none else 0,  # start unselected if allow_none
                key=key_name,
                help=help_text,
                horizontal=columns)

        answers[key_name] = None if selected == "None" else selected

    elif input_type == "checkbox":
        st.write(question)
        if help_text:
            st.caption(help_text)

        selected = []

        if columns:
            cols_list = st.columns(len(options))
        else:
            cols_list = [st] * len(options)  # ✅ repeat st for each option

        for col, option in zip(cols_list, options):
            if col.checkbox(option, key=f"{key_name}_{option}"):
                selected.append(option)

        answers[key_name] = selected

    elif input_type == "date":
        answers[key_name] = st.date_input(question, key=key_name, help=help_text)

    return answers[key_name]





def clean_value(value):
    if value is None or value == [] or value=='':
        return "Not Answered"
    return value
































def generate_pdf(answers_dict,email):
    import datetime
    from fpdf import FPDF

    name = answers_dict.get("name", "questionnaire").replace(" ", "_")
    filename = f"{name}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    for key, value in answers_dict.items():
        # =========================
        # ESTIMATED TAX
        # =========================
        if key.lower() == "estimatedtax" and isinstance(value, dict):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Estimated Tax Payments", ln=True)
            pdf.set_font("Arial", "", 11)

            col_width = pdf.w / 2 - 15

            def get_vals(q):
                return (
                    value.get(f"{q}_2025_FD", 0),
                    value.get(f"{q}_2025_CA", 0)
                )

            quarters = ["Q1", "Q2", "Q3", "Q4"]

            for i in range(0, 4, 2):
                q_left = quarters[i]
                q_right = quarters[i + 1]

                fd_l, ca_l = get_vals(q_left)
                fd_r, ca_r = get_vals(q_right)

                x_start = pdf.get_x()
                y_start = pdf.get_y()

                pdf.multi_cell(col_width, 6,
                    f"{q_left} 2025\nFederal: {fd_l}\nCA: {ca_l}",
                    border=1
                )

                pdf.set_xy(x_start + col_width, y_start)

                pdf.multi_cell(col_width, 6,
                    f"{q_right} 2025\nFederal: {fd_r}\nCA: {ca_r}",
                    border=1
                )
                pdf.ln(2)
            continue
        if key == "schedule_c_details" and isinstance(value, list):

            expense_order = [
                "advertising","office_expenses","contract_labor",
                "pension_and_profit_sharing","commission_and_fees",
                "rent_or_lease","depletion","repairs_and_maintenance",
                "employee_benefits_programs","supplies","health_insurance",
                "taxes_and_licenses","insurance_other_than_health","travel",
                "mortgage_interest","meals_and_entertainment","other_interest",
                "utilities","legal_and_professional_services","wages"
            ]

            def labelize(k):
                return k.replace("_", " ").title()

            col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 4
            row_h = 7

            for i, biz in enumerate(value):

                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 7, f"Business #{i+1}", ln=True)
                pdf.ln(1)

                # =========================
                # INCOME SECTION
                # =========================
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 6, "Income", ln=True)
                pdf.set_font("Arial", "", 9)

                income_fields = [
                    "1099_nec_amounts",
                    "1099_k_amounts",
                    "1099_misc_amounts",
                    "other_cash_income",
                    "business_type",
                    "other_business"
                ]

                for k in income_fields:
                    if k in biz:
                        v = biz.get(k)

                        if hasattr(v, "strftime"):
                            v = v.strftime("%Y-%m-%d")

                        v = clean_value(v)

                        pdf.cell(70, 6, f"{labelize(k)}:", border=0)
                        pdf.cell(0, 6, str(v), ln=True)

                pdf.ln(2)


                # =========================
                # EXPENSE TABLE
                # =========================
                pdf.set_font("Arial", "B", 9)

                headers = ["Expense", "Amount", "Expense", "Amount"]
                for h in headers:
                    pdf.cell(col_w, row_h, h, border=1, align="C")
                pdf.ln()

                pdf.set_font("Arial", "", 9)

                ordered = [
                    (k, clean_value(biz.get(k, 0)))
                    for k in expense_order if k in biz
                ]

                odd, even = [], []

                for k, v in ordered:
                    if (expense_order.index(k) + 1) % 2:
                        odd.append((k, v))
                    else:
                        even.append((k, v))

                max_len = max(len(odd), len(even))

                for idx in range(max_len):

                    l = odd[idx] if idx < len(odd) else ("", "")
                    r = even[idx] if idx < len(even) else ("", "")

                    pdf.cell(col_w, row_h, labelize(l[0]) if l else "", border=1)
                    pdf.cell(col_w, row_h, str(l[1]) if l else "", border=1)

                    pdf.cell(col_w, row_h, labelize(r[0]) if r else "", border=1)
                    pdf.cell(col_w, row_h, str(r[1]) if r else "", border=1)

                    pdf.ln(row_h)

                pdf.ln(4)
                # =========================
                # VEHICLE SECTION
                # =========================
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 6, "Vehicle Information", ln=True)
                pdf.set_font("Arial", "", 9)

                vehicle_fields = [
                    "SCH_C_vehicle_desc",
                    "SCH_C_vehicle_date",
                    "buesiness_miles",
                    "SCH_C_vehicle_other",
                    "SCH_C_vehicle_off_duty",
                    "SCH_C_vehicle_evidence"
                ]
                for k in vehicle_fields:
                    if k in biz:
                        v = biz.get(k)
                        if hasattr(v, "strftime"):
                            v = v.strftime("%Y-%m-%d")
                        v = clean_value(v)
                        pdf.cell(70, 6, f"{labelize(k)}:", border=0)
                        pdf.cell(0, 6, str(v), ln=True)
                pdf.ln(2)
            continue
        if key == "CDCC_details":
            children = (value or {}).get("children") or []
            if isinstance(children, list) and len(children) > 0:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Child & Dependent Care Credit (CDCC)", ln=True)
                pdf.ln(2)
                tax_year = int(answers_dict.get("tax_year", 2024))
                ref_date = datetime.date(tax_year, 12, 31)
                for i, child in enumerate(children, start=1):
                    if not isinstance(child, dict):
                        continue
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 7, f"Child #{i}", ln=True)
                    # ================= CHILD =================
                    name = child.get("name") or "N/A"
                    birthday = child.get("birthday")
                    if isinstance(birthday, datetime.date):
                        age = (
                            ref_date.year
                            - birthday.year
                            - ((ref_date.month, ref_date.day) <
                            (birthday.month, birthday.day))
                        )
                        status = "Over 13" if isinstance(age, int) and age >= 13 else "OK"
                    else:
                        age = "N/A"
                        status = "Missing DOB"

                    pdf.set_font("Arial", "", 10)
                    pdf.cell(50, 6, "Name:", border=0)
                    pdf.cell(0, 6, str(name), ln=True)

                    pdf.cell(50, 6, "Birthday:", border=0)
                    pdf.cell(0, 6, str(birthday) if birthday else "N/A", ln=True)

                    pdf.cell(50, 6, "Age:", border=0)
                    pdf.cell(0, 6, str(age), ln=True)

                    pdf.cell(50, 6, "Status:", border=0)
                    pdf.cell(0, 6, str(status), ln=True)

                    pdf.ln(2)

                    # ================= PROVIDER =================
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 6, "Provider Information", ln=True)

                    pdf.set_font("Arial", "", 10)

                    pdf.cell(50, 6, "ID Type:", border=0)
                    pdf.cell(0, 6, child.get("provider_id_type") or "N/A", ln=True)

                    pdf.cell(50, 6, "Name:", border=0)
                    pdf.cell(0, 6, child.get("provider_name") or "N/A", ln=True)

                    pdf.cell(50, 6, "Address:", border=0)
                    pdf.cell(0, 6, child.get("provider_address") or "N/A", ln=True)

                    pdf.cell(50, 6, "Phone:", border=0)
                    pdf.cell(0, 6, child.get("provider_phone") or "N/A", ln=True)

                    pdf.cell(50, 6, "Amount Paid:", border=0)
                    pdf.cell(0, 6, str(child.get("amount_paid") or 0), ln=True)

                    # flags
                    flags = child.get("provider_flags") or []
                    if isinstance(flags, list):
                        flags = ", ".join(flags)

                    pdf.cell(50, 6, "Flags:", border=0)
                    pdf.cell(0, 6, flags or "None", ln=True)

                    pdf.ln(5)

                pdf.ln(3)

            continue
        # =========================
        # EDUCATION CREDITS
        # =========================
        if key == "EducationCredits":
            students = (value or {}).get("students") or []

            if isinstance(students, list) and len(students) > 0:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Education Credits (1098-T)", ln=True)
                pdf.ln(2)

                for i, stu in enumerate(students, start=1):
                    if not isinstance(stu, dict):
                        continue

                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 7, f"Student #{i}", ln=True)

                    pdf.set_font("Arial", "", 10)

                    # ================= BASIC =================
                    pdf.cell(60, 6, "Name:", border=0)
                    pdf.cell(0, 6, stu.get("name") or "N/A", ln=True)

                    pdf.cell(60, 6, "Relationship:", border=0)
                    pdf.cell(0, 6, stu.get("relationship") or "N/A", ln=True)

                    pdf.cell(60, 6, "Age:", border=0)
                    pdf.cell(0, 6, str(stu.get("age") or "N/A"), ln=True)

                    pdf.ln(2)

                    # ================= STATUS =================
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 6, "Student Status", ln=True)

                    pdf.set_font("Arial", "", 10)

                    pdf.cell(60, 6, "Enrollment:", border=0)
                    pdf.cell(0, 6, stu.get("enrollment_status") or "N/A", ln=True)

                    pdf.cell(60, 6, "Level:", border=0)
                    pdf.cell(0, 6, stu.get("level") or "N/A", ln=True)

                    pdf.cell(60, 6, "Years Post-Secondary:", border=0)
                    pdf.cell(0, 6, str(stu.get("years_post_secondary") or "0"), ln=True)

                    pdf.ln(2)

                    # ================= ELIGIBILITY =================
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 6, "Eligibility", ln=True)

                    pdf.set_font("Arial", "", 10)

                    pdf.cell(60, 6, "Felony Drug Conviction:", border=0)
                    pdf.cell(0, 6, stu.get("felony_drug") or "N/A", ln=True)

                    pdf.cell(60, 6, "AOTC > 4 Years:", border=0)
                    pdf.cell(0, 6, stu.get("aotc_4_years") or "N/A", ln=True)

                    pdf.cell(60, 6, "Box 4 or 6:", border=0)
                    pdf.cell(0, 6, stu.get("box4_or_6") or "N/A", ln=True)

                    pdf.ln(2)

                    # ================= FINANCIAL =================
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 6, "Education Amounts", ln=True)

                    pdf.set_font("Arial", "", 10)

                    pdf.cell(60, 6, "Box 1 Payments:", border=0)
                    pdf.cell(0, 6, str(stu.get("payments_box1") or 0), ln=True)

                    pdf.cell(60, 6, "Box 5 Scholarships:", border=0)
                    pdf.cell(0, 6, str(stu.get("scholarships_box5") or 0), ln=True)

                    pdf.cell(60, 6, "Additional Expenses:", border=0)
                    pdf.cell(0, 6, str(stu.get("additional_qualified_expenses_amount") or 0), ln=True)

                    pdf.cell(60, 6, "Qualified Expenses:", border=0)
                    pdf.cell(0, 6, str(stu.get("qualified_expenses") or 0), ln=True)

                    # ================= RESULT =================
                    qee = stu.get("qualified_expenses", 0)

                    pdf.ln(1)
                    if qee > 0:
                        pdf.cell(0, 6, "Result: Qualified education expenses eligible", ln=True)
                    elif qee < 0:
                        pdf.cell(0, 6, "Result: Possible taxable scholarship income", ln=True)
                    else:
                        pdf.cell(0, 6, "Result: No net qualified expenses", ln=True)

                    pdf.ln(5)

                pdf.ln(3)

            continue
        # =========================
        # DEFAULT
        # =========================

        val=safe_one_line(clean_value(value))
        if "{" not in str(val):
            pdf.cell(70, 6, f"{key.replace('_',' ').title()}:", border=0)
            pdf.cell(0, 6, val, ln=True)

    if email==True:
        pdf.output(filename)
        return filename
    else:
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        return pdf_bytes