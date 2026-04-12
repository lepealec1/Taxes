    
    
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
import time

if st.session_state.step == "success":
    st.success("✔ Email sent successfully!")
    st.toast("Your PDF has been delivered 📧", icon="✅")
    st.balloons()

    if st.button("Send another PDF"):
        st.session_state.step = "form"
        st.rerun()

    st.stop()

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
















import streamlit as st
import smtplib
from email.message import EmailMessage
import os

uploaded_file = st.file_uploader("Upload a document (optional)")

def send_email(pdf_file=None):
    global uploaded_file
    TO_EMAIL = "lepealec518@gmail.com"
    EMAIL_ADDRESS = st.secrets["email"]["user"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]
    
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





# -----------------------
# Function definition
# -----------------------
import time
import streamlit as st
import random

# -----------------------
# Session state init
# -----------------------
if "captcha_question" not in st.session_state:
    def generate_captcha():
        a = random.randint(1, 49)
        b = random.randint(1, 49)
        return f"{a} + {b}", str(a + b)

    q, a = generate_captcha()
    st.session_state.captcha_question = q
    st.session_state.captcha_answer = a


# -----------------------
# CAPTCHA input
# -----------------------
user_captcha = st.text_input(
    f"🔒 What is {st.session_state.captcha_question}?"
)


# -----------------------
# Submit logic
# -----------------------
def handle_submit():
    if user_captcha.strip() != st.session_state.captcha_answer:
        st.error("❌ Incorrect answer. Try again.")
        return

    pdf_file = generate_pdf(answers)

    try:
        send_email(pdf_file)

        # 🔥 set success step
        st.session_state.step = "success"

        # regenerate CAPTCHA for next time
        a = random.randint(1, 49)
        b = random.randint(1, 49)

        st.session_state.captcha_question = f"{a} + {b}"
        st.session_state.captcha_answer = str(a + b)

        st.rerun()

    except Exception as e:
        st.error(f"Failed to send email: {e}")

# -----------------------
# Button
# -----------------------
if st.button("Generate PDF & Email (One Email Per Session)"):
    handle_submit()


st.warning("One submit per correct captcha")


if "step" not in st.session_state:
    st.session_state.step = "form"  # form | success
