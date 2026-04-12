import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import datetime
import textwrap
import streamlit as st
from fpdf import FPDF
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
yes_no=['Yes','No']
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
    name = answers_dict.get("name", "questionnaire").replace(" ", "_")
    filename = f"{name}.pdf"
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    label_width = 70
    value_width = page_width - label_width
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    for key, value in answers_dict.items():
        # Check for nested list of dictionaries
        if key in ["schedule_c_details", "ssa_lump_sum_details"] and isinstance(value, list):
            for i, row in enumerate(value):
                for sub_key, sub_val in row.items():
                    sub_val = clean_value(sub_val)
                    pdf.cell(label_width, 6, f"{sub_key}_{i+1}:", border=0)
                    pdf.cell(value_width, 6, safe_one_line(sub_val), border=0, ln=True)
        # Handle EstimatedTax specifically (it's a dictionary)
        elif key == "EstimatedTax" and isinstance(value, dict):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Estimated Tax Payments", ln=True)
            pdf.set_font("Arial", "", 11)
            col_width = pdf.w / 2 - 15  # 2 columns
            row_height = 10
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
                # Left column
                x_start = pdf.get_x()
                y_start = pdf.get_y()
                pdf.multi_cell(
                    col_width,
                    6,
                    f"{q_left} 2025\nFederal: {fd_l}\nCA: {ca_l}",
                    border=1
                )
                # Right column (same row)
                pdf.set_xy(x_start + col_width, y_start)
                pdf.multi_cell(
                    col_width,
                    6,
                    f"{q_right} 2025\nFederal: {fd_r}\nCA: {ca_r}",
                    border=1
                )
                pdf.ln(1)  # spacing between rows
                # Handle other simple values
            else:
                if key.lower!="estimatedtax": 
                    value = clean_value(value)
                    pdf.cell(label_width, 6, f"{key}:", border=0)
                    pdf.cell(value_width, 6, safe_one_line(value), border=0, ln=True)

        if key.lower!="estimatedtax":
            value = clean_value(value)
            pdf.cell(label_width, 6, f"{key.replace('_',' ').title()}:", border=0)
            pdf.cell(value_width, 6, safe_one_line(value), border=0, ln=True)
    pdf.output(filename)
    return filename 



def generate_pdf(answers_dict):
    name = answers_dict.get("name", "questionnaire").replace(" ", "_")
    filename = f"{name}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin
    label_width = 70
    value_width = page_width - label_width

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    for key, value in answers_dict.items():

        # =========================
        # ESTIMATED TAX TABLE
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

                pdf.multi_cell(
                    col_width,
                    6,
                    f"{q_left} 2025\nFederal: {fd_l}\nCA: {ca_l}",
                    border=1
                )

                pdf.set_xy(x_start + col_width, y_start)

                pdf.multi_cell(
                    col_width,
                    6,
                    f"{q_right} 2025\nFederal: {fd_r}\nCA: {ca_r}",
                    border=1
                )

                pdf.ln(2)

            continue  # ⭐ CRITICAL: prevents raw dict printing

        # =========================
        # SPECIAL LIST STRUCTURES
        # =========================
        if key == "schedule_c_details" and isinstance(value, list):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Schedule C - Self Employment", ln=True)
            pdf.ln(2)

            col1_width = 70
            col2_width = pdf.w - pdf.l_margin - pdf.r_margin - col1_width
            row_height = 6

            for i, biz in enumerate(value):
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 7, f"Business #{i+1}", ln=True)
                pdf.ln(1)

                pdf.set_font("Arial", "", 10)

                for sub_key, sub_val in biz.items():
                    sub_val = clean_value(sub_val)
                    label = sub_key.replace("_", " ").title()

                    x = pdf.get_x()
                    y = pdf.get_y()

                    # LEFT CELL (label)
                    pdf.multi_cell(col1_width, row_height, label, border=1)

                    # RIGHT CELL (value aligned to same row)
                    pdf.set_xy(x + col1_width, y)
                    pdf.multi_cell(col2_width, row_height, safe_one_line(sub_val), border=1)

                    # IMPORTANT: force row alignment
                    pdf.set_y(y + max(row_height, pdf.font_size * 1.5))

                pdf.ln(3)

            continue
        if key in ["ssa_lump_sum_details"] and isinstance(value, list):
            for i, row in enumerate(value):
                for sub_key, sub_val in row.items():
                    sub_val = clean_value(sub_val)
                    pdf.cell(label_width, 6, f"{sub_key}_{i+1}:", border=0)
                    pdf.cell(value_width, 6, safe_one_line(sub_val), border=0, ln=True)

            continue

        # =========================
        # DEFAULT FIELDS
        # =========================
        value = clean_value(value)
        pdf.cell(label_width, 6, f"{key.replace('_',' ').title()}:", border=0)
        pdf.cell(value_width, 6, safe_one_line(value), border=0, ln=True)

    pdf.output(filename)
    return filename





def generate_pdf(answers_dict):
    name = answers_dict.get("name", "questionnaire").replace(" ", "_")
    filename = f"{name}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin
    label_width = 70
    value_width = page_width - label_width

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

                pdf.multi_cell(
                    col_width,
                    6,
                    f"{q_left} 2025\nFederal: {fd_l}\nCA: {ca_l}",
                    border=1
                )

                pdf.set_xy(x_start + col_width, y_start)

                pdf.multi_cell(
                    col_width,
                    6,
                    f"{q_right} 2025\nFederal: {fd_r}\nCA: {ca_r}",
                    border=1
                )

                pdf.ln(2)

            continue

        # =========================
        # SCHEDULE C
        # =========================
        if key == "schedule_c_details" and isinstance(value, list):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Schedule C - Self Employment", ln=True)
            pdf.ln(2)

            # =========================
            # IRS ORDER (DATA KEYS ONLY)
            # =========================
            expense_order = [
                "advertising",
                "office_expenses",
                "contract_labor",
                "pension_and_profit_sharing",
                "commission_and_fees",
                "rent_or_lease",
                "depletion",
                "repairs_and_maintenance",
                "employee_benefits_programs",
                "supplies",
                "health_insurance",
                "taxes_and_licenses",
                "insurance_other_than_health",
                "travel",
                "mortgage_interest",
                "meals_and_entertainment",
                "other_interest",
                "utilities",
                "legal_and_professional_services",
                "wages"
            ]

            col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 4
            row_h = 7

            def labelize(k):
                return k.replace("_", " ").title()

            for i, biz in enumerate(value):
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 7, f"Business #{i+1}", ln=True)
                pdf.ln(1)

                pdf.set_font("Arial", "", 9)

                # =========================
                # HEADER
                # =========================
                pdf.set_font("Arial", "B", 9)
                headers = ["Expense", "Amount", "Expense", "Amount"]

                for h in headers:
                    pdf.cell(col_w, row_h, h, border=1, align="C")
                pdf.ln()

                pdf.set_font("Arial", "", 9)

                # =========================
                # BUILD ORDERED EXPENSE LIST
                # =========================
                ordered = []
                for k in expense_order:
                    if k in biz:
                        ordered.append((k, clean_value(biz.get(k, 0))))

                # =========================
                # SPLIT INTO ODD / EVEN
                # =========================
                odd_items = []
                even_items = []

                for k, v in ordered:
                    num = expense_order.index(k) + 1  # stable IRS position

                    if num % 2 == 1:
                        odd_items.append((k, v))
                    else:
                        even_items.append((k, v))

                # =========================
                # 4-COLUMN GRID OUTPUT
                # =========================
                max_len = max(len(odd_items), len(even_items))

                for idx in range(max_len):
                    left = odd_items[idx] if idx < len(odd_items) else ("", "")
                    right = even_items[idx] if idx < len(even_items) else ("", "")

                    pdf.cell(col_w, row_h, labelize(left[0]) if left else "", border=1)
                    pdf.cell(col_w, row_h, str(left[1]) if left else "", border=1)

                    pdf.cell(col_w, row_h, labelize(right[0]) if right else "", border=1)
                    pdf.cell(col_w, row_h, str(right[1]) if right else "", border=1)

                    pdf.ln(row_h)

                pdf.ln(3)

                # =========================
                # NON-EXPENSE FIELDS
                # =========================
                for k, v in biz.items():
                    if k in expense_order:
                        continue

                    v = clean_value(v)
                    label = k.replace("_", " ").title()

                    pdf.cell(70, 6, f"{label}:", border=0)
                    pdf.cell(0, 6, safe_one_line(v), ln=True)

                pdf.ln(3)

            continue
        # =========================
        # SSA DETAILS
        # =========================
        if key == "ssa_lump_sum_details" and isinstance(value, list):
            for i, row in enumerate(value):
                for sub_key, sub_val in row.items():
                    sub_val = clean_value(sub_val)
                    pdf.cell(label_width, 6, f"{sub_key}_{i+1}:", border=0)
                    pdf.cell(value_width, 6, safe_one_line(sub_val), border=0, ln=True)

            continue

        # =========================
        # DEFAULT FIELDS
        # =========================
        value = clean_value(value)
        pdf.cell(label_width, 6, f"{key.replace('_',' ').title()}:", border=0)
        pdf.cell(value_width, 6, safe_one_line(value), border=0, ln=True)

    pdf.output(filename)
    return filename































def generate_pdf(answers_dict):
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

        # =========================
        # SCHEDULE C
        # =========================
        if key == "schedule_c_details" and isinstance(value, list):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Schedule C - Self Employment", ln=True)
            pdf.ln(2)

            expense_order = [
                "advertising","office_expenses","contract_labor",
                "pension_and_profit_sharing","commission_and_fees",
                "rent_or_lease","depletion","repairs_and_maintenance",
                "employee_benefits_programs","supplies","health_insurance",
                "taxes_and_licenses","insurance_other_than_health","travel",
                "mortgage_interest","meals_and_entertainment","other_interest",
                "utilities","legal_and_professional_services","wages"
            ]

            col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 4
            row_h = 7

            def labelize(k):
                return k.replace("_", " ").title()

            for i, biz in enumerate(value):
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 7, f"Business #{i+1}", ln=True)
                pdf.ln(1)

                pdf.set_font("Arial", "B", 9)
                headers = ["Expense", "Amount", "Expense", "Amount"]

                for h in headers:
                    pdf.cell(col_w, row_h, h, border=1, align="C")
                pdf.ln()

                pdf.set_font("Arial", "", 9)

                ordered = [(k, clean_value(biz.get(k, 0))) for k in expense_order if k in biz]

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

                pdf.ln(3)

            continue

        # =========================
        # CDCC (FINAL CLEAN VERSION)
        # =========================
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
        # DEFAULT
        # =========================
        pdf.cell(70, 6, f"{key.replace('_',' ').title()}:", border=0)
        pdf.cell(0, 6, safe_one_line(clean_value(value)), ln=True)

    pdf.output(filename)
    return filename