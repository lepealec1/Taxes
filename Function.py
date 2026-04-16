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
































def generate_pdf(answers_dict):
    import datetime
    from fpdf import FPDF

    def clean(v):
        return "" if v is None else str(v)

    name = answers_dict.get("name", "questionnaire").replace(" ", "_")
    filename = f"{name}.pdf"

    filename = f"abc.pdf"
    
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
            quarters = ["Q1", "Q2", "Q3", "Q4"]

            def get_vals(q):
                return (
                    value.get(f"{q}_2025_FD", 0),
                    value.get(f"{q}_2025_CA", 0)
                )

            for i in range(0, 4, 2):
                q1, q2 = quarters[i], quarters[i + 1]

                x = pdf.get_x()
                y = pdf.get_y()

                fd1, ca1 = get_vals(q1)
                fd2, ca2 = get_vals(q2)

                pdf.multi_cell(col_width, 6,
                    f"{q1} 2025\nFederal: {fd1}\nCA: {ca1}",
                    border=1
                )

                pdf.set_xy(x + col_width, y)

                pdf.multi_cell(col_width, 6,
                    f"{q2} 2025\nFederal: {fd2}\nCA: {ca2}",
                    border=1
                )

                pdf.ln(2)

            continue

        # =========================
        # SCHEDULE C DETAILS
        # =========================
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

                # Income
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
                        v = clean(biz.get(k))
                        pdf.cell(70, 6, f"{labelize(k)}:", border=0)
                        pdf.cell(0, 6, v, ln=True)

                pdf.ln(2)

                # Expense table
                pdf.set_font("Arial", "B", 9)
                headers = ["Expense", "Amount", "Expense", "Amount"]

                for h in headers:
                    pdf.cell(col_w, row_h, h, border=1, align="C")
                pdf.ln()

                pdf.set_font("Arial", "", 9)

                ordered = [(k, clean(biz.get(k, 0))) for k in expense_order if k in biz]

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

                    pdf.cell(col_w, row_h, labelize(l[0]) if l[0] else "", border=1)
                    pdf.cell(col_w, row_h, str(l[1]) if l[1] else "", border=1)

                    pdf.cell(col_w, row_h, labelize(r[0]) if r[0] else "", border=1)
                    pdf.cell(col_w, row_h, str(r[1]) if r[1] else "", border=1)

                    pdf.ln(row_h)

                pdf.ln(4)

                # Vehicle
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
                        pdf.cell(70, 6, f"{labelize(k)}:", border=0)
                        pdf.cell(0, 6, clean(biz.get(k)), ln=True)

                pdf.ln(2)

            continue

        # =========================
        # CDCC
        # =========================
        if key == "CDCC_details":
            children = (value or {}).get("children") or []

            if isinstance(children, list) and children:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Child & Dependent Care Credit", ln=True)
                pdf.ln(2)

                tax_year = int(answers_dict.get("tax_year", 2024))
                ref_date = datetime.date(tax_year, 12, 31)

                for i, child in enumerate(children, start=1):
                    if not isinstance(child, dict):
                        continue

                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 7, f"Child #{i}", ln=True)
                    pdf.set_font("Arial", "", 10)

                    name = child.get("name") or "N/A"
                    birthday = child.get("birthday")

                    if isinstance(birthday, datetime.date):
                        age = ref_date.year - birthday.year
                    else:
                        age = "N/A"

                    pdf.cell(50, 6, "Name:", border=0)
                    pdf.cell(0, 6, str(name), ln=True)

                    pdf.cell(50, 6, "Age:", border=0)
                    pdf.cell(0, 6, str(age), ln=True)

                    pdf.ln(3)

            continue

        # =========================
        # EDUCATION
        # =========================
        if key == "EducationCredits":
            students = (value or {}).get("students") or []

            if students:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Education Credits", ln=True)
                pdf.ln(2)

                for i, stu in enumerate(students, 1):
                    if not isinstance(stu, dict):
                        continue

                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 7, f"Student #{i}", ln=True)
                    pdf.set_font("Arial", "", 10)

                    pdf.cell(60, 6, "Name:", border=0)
                    pdf.cell(0, 6, stu.get("name") or "N/A", ln=True)

                    pdf.cell(60, 6, "Expenses:", border=0)
                    pdf.cell(0, 6, str(stu.get("qualified_expenses") or 0), ln=True)

                    pdf.ln(3)

            continue

        # =========================
        # DEFAULT
        # =========================
        if not isinstance(value, (dict, list)):
            pdf.cell(70, 6, f"{key.replace('_',' ').title()}:", border=0)
            pdf.cell(0, 6, clean(value), ln=True)

    # =========================
    # IMPORTANT: STREAMLIT SAFE OUTPUT
    # =========================
    pdf_bytes = pdf.output(dest="S").encode("latin-1")

    return {
        "pdf_bytes": pdf_bytes,
        "filename": filename
    }