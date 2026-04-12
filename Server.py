# C:\Users\alepe\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run c:\repos\Taxes\Local.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import datetime
import textwrap
import streamlit as st
from fpdf import FPDF
from BasicInfo import BasicInfo, answers
import os
import pickle


from Function import ask_question, generate_pdf



st.title("VITA Supplemental Questionnaire")

from BasicInfo import BasicInfo
from BasicInfo import HealthInsurance
from BasicInfo import CaResidency
from BasicInfo import MiscQuestions
from BasicInfo import answers
from BasicInfo import Disclaimers, Income, RequiredDocuments,F1099R,SSA, OtherIncome
from BasicInfo import SchC, SchD, Deductions, CDCC, EducationCredits, RefundAndPayment

Disclaimers()
RequiredDocuments()
BasicInfo()
HealthInsurance()
CaResidency()
MiscQuestions()


with st.expander("Income", expanded=False):
    Income()
    F1099R()
    SSA()
    SchC()
    SchD()
    OtherIncome()


with st.expander("Deductions & Credits", expanded=False):
    Deductions()
    CDCC()
    EducationCredits()


RefundAndPayment()




def format_value(value, max_width=90):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)

    if isinstance(value, dict):
        value = "\n".join(f"{k}: {format_value(v)}" for k, v in value.items())

    text = str(value)

    wrapped = []
    for line in text.split("\n"):
        words = line.split(" ")
        rebuilt = []

        for word in words:
            if len(word) > max_width:
                rebuilt.append("\n".join(textwrap.wrap(word, max_width)))
            else:
                rebuilt.append(word)

        wrapped.append(" ".join(rebuilt))

    return "\n".join(wrapped)


from fpdf import FPDF
import datetime
import textwrap


def format_value(value, max_width=90):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)

    if isinstance(value, dict):
        value = " | ".join(f"{k}: {format_value(v)}" for k, v in value.items())

    text = str(value)

    wrapped = []
    for line in text.split("\n"):
        words = line.split(" ")
        rebuilt = []

        for word in words:
            if len(word) > max_width:
                rebuilt.append("\n".join(textwrap.wrap(word, max_width)))
            else:
                rebuilt.append(word)

        wrapped.append(" ".join(rebuilt))

    return "\n".join(wrapped)

from fpdf import FPDF
import datetime
import textwrap




from fpdf import FPDF
import datetime
import textwrap


def safe_text(value, width=80):
    text = str(value)

    # break by lines first
    lines = text.split("\n")
    result = []

    for line in lines:
        words = line.split(" ")
        rebuilt = []

        for word in words:
            # CRITICAL FIX: break unspaced long strings
            if len(word) > width:
                rebuilt.append("\n".join(textwrap.wrap(word, width)))
            else:
                rebuilt.append(word)

        result.append(" ".join(rebuilt))

    return "\n".join(result)

from fpdf import FPDF
import datetime


from fpdf import FPDF
import datetime


def safe_one_line(value, max_len=120):
    if isinstance(value, datetime.date):
        value = value.strftime("%Y-%m-%d")

    text = str(value)

    if len(text) > max_len:
        text = text[:max_len] + "..."

    return text


















if st.button("Send Email"):
        try:
            # Create email
            msg = EmailMessage()
            msg["Subject"] = "Tax"
            msg["From"] = "lepealec518@gmail.com"
            msg["To"] = "lepealec518@gmail.com"
            body="Document"
            msg.set_content(body)

            # Attach file
            file_data = uploaded_file.read()
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=uploaded_file.name
            )

            # Send via Gmail SMTP
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login("your_email@gmail.com", "your_app_password")
                smtp.send_message(msg)

            st.success("Email sent successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import smtplib
from email.message import EmailMessage
import os

uploaded_file = st.file_uploader("Upload a document")

def send_email(pdf_file=None):
    global uploaded_file
    TO_EMAIL = "lepealec518@gmail.com"
    EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = answers.get('name', 'User') + " Tax Questionnaire PDF"
    msg.set_content("Attached files.")

    # ✅ Attach uploaded file (only if it exists)
    if uploaded_file is not None:
        file_data = uploaded_file.read()
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=uploaded_file.name
        )

    # ✅ Attach generated PDF (only if it exists)
    if pdf_file and os.path.exists(pdf_file):
        with open(pdf_file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_file)
            )

    # ❌ Prevent sending empty email
    if uploaded_file is None and not (pdf_file and os.path.exists(pdf_file)):
        st.warning("No file to send.")
        return

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    st.success("Email sent!")


# --- Streamlit UI ---
if st.button("Generate PDF & Email"):
    pdf_file = generate_pdf(answers)
    st.success(f"PDF generated: {pdf_file}")

    try:
        send_email(pdf_file)
        st.success("PDF sent to generic email!")
        st.balloons()
    except Exception as e:
        st.error(f"Failed to send email: {e}")


        

