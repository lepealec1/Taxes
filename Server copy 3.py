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
from BasicInfo import Disclaimers, Income, RequiredDocuments,F1099R,SSA
from BasicInfo import SchC, SchD, Deductions, CDCC


Disclaimers()
RequiredDocuments()
BasicInfo()
#HealthInsurance()
#CaResidency()
#MiscQuestions()
#with st.expander("Income", expanded=False):
#    Income()
#    F1099R()
#    SSA()
#    SchC()
#    SchD()

with st.expander("Deductions & Credits", expanded=False):
    Deductions()    
    CDCC()


uploaded_file = st.file_uploader("Upload a document")







def send_email(pdf_file):
    # Generic email to send to
    TO_EMAIL = "lepealec518@gmail.com"  # replace with your generic email

    # Your Gmail account (or app password)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = answers['name']+"Tax Questionnaire PDF"

    # Attach the PDF
    with open(pdf_file, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={pdf_file}")
    msg.attach(part)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)





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


        

