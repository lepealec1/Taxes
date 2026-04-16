# C:\Users\alepe\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run c:\repos\Taxes\Local.py
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
from fpdf import FPDF
import time, pickle, os, textwrap, datetime, smtplib, random

st.title("VITA Supplemental Questionnaire v1")

from BasicInfo import MiscQuestions, answers, CaResidency, HealthInsurance, BasicInfo
from BasicInfo import Disclaimers, Income, RequiredDocuments,F1099R,SSA, OtherIncome
from BasicInfo import SchC, SchD, Deductions, CDCC, EducationCredits, RefundAndPayment, FinalDisclaimer, FinalNotes
from Function import ask_question, generate_pdf

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
FinalNotes()
FinalDisclaimer()

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
def safe_one_line(value, max_len=120):
    if isinstance(value, datetime.date):
        value = value.strftime("%Y-%m-%d")

    text = str(value)

    if len(text) > max_len:
        text = text[:max_len] + "..."

    return text
uploaded_file = st.file_uploader("Upload a document (optional)")
def send_email(pdf_file=None):
    st.write("pdf_file:", pdf_file)

    global uploaded_file

    TO_EMAIL = "lepealec518@gmail.com"
    EMAIL_ADDRESS = st.secrets["email"]["user"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = answers.get('name', 'User') + " Tax Questionnaire PDF"
    msg.set_content("Attached files.")

    # ✅ uploaded file (if exists)
    if uploaded_file is not None:
        msg.add_attachment(
            uploaded_file.read(),
            maintype="application",
            subtype="octet-stream",
            filename=uploaded_file.name
        )

    # ✅ GENERATED PDF (FIXED)
    if pdf_file:
        msg.add_attachment(
            pdf_file["pdf_bytes"],   # 🔥 THIS is the fix
            maintype="application",
            subtype="pdf",
            filename=pdf_file["filename"]
        )

    # ❌ prevent empty email
    if uploaded_file is None and pdf_file is None:
        st.warning("No file to send.")
        return

    # send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    st.success("Email sent!")
st.warning("The button will also send attachments if any are included.")
st.warning("One submission per correct CAPTCHA.")

st.metric("📧 Emails Sent Successfully:", st.session_state.email_count)


from datetime import date


result = generate_pdf(answers)

today = date.today().strftime("%Y-%m-%d")

st.download_button(
    "Download PDF",
    data=result["pdf_bytes"],
    file_name=f"{answers.get('tax_year'),'_',answers.get('name')}_VITA_Questionnaire_{today}.pdf",
    mime="application/pdf"
)    