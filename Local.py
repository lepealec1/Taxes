# C:\Users\alepe\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe run c:\repos\Taxes\Local.py


import streamlit as st
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from BasicInfo import BasicInfo, answers
import os
import pickle


from Function import ask_question

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        # Headless authorization for Streamlit Cloud
        creds = flow.run_local_server(port=0, open_browser=False)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build('drive', 'v3', credentials=creds)

# ----------------------------
# PDF generation
# ----------------------------
def generate_pdf(answers_dict, filename="questionnaire.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Supplemental Questionnaire", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    for key, value in answers_dict.items():
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        pdf.multi_cell(0, 8, f"{key.replace('_',' ').title()}: {value}")
        pdf.ln(1)
    pdf.output(filename)
    return filename

st.title("PDF Tax + Google Drive Upload")

from BasicInfo import BasicInfo
from BasicInfo import HealthInsurance
from BasicInfo import CaResidency
from BasicInfo import MiscQuestions
from BasicInfo import answers
from BasicInfo import Disclaimers, Income, RequiredDocuments,F1099R,SSA
from BasicInfo import SchC, SchD


Disclaimers()
RequiredDocuments()
BasicInfo()
HealthInsurance()
CaResidency()
MiscQuestions()
#with st.expander("Income", expanded=False):
 #   Income()
  #  F1099R()
   # SSA()
    #SchC()
#    SchD()

with st.expander("Deductions & Credits", expanded=True):
    SchD()    

def send_email(pdf_file):
    # Generic email to send to
    TO_EMAIL = "lepealec518@gmail.com"  # replace with your generic email

    # Your Gmail account (or app password)
    EMAIL_ADDRESS = "lepealec518@gmail.com"
    EMAIL_PASSWORD = "jezv tutk apta lfko"

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


        