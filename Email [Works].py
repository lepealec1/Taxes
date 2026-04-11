import streamlit as st
from fpdf import FPDF
from BasicInfo import BasicInfo, answers

# --- Collect answers ---
BasicInfo()

# --- Generate PDF ---
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

# --- Email PDF ---
def send_email(pdf_file):
    # Generic email to send to
    TO_EMAIL = "lepealec518@gmail.com"  # replace with your generic email

    # Your Gmail account (or app password)
    EMAIL_ADDRESS = st.secrets["email"]["user"]
    EMAIL_PASSWORD = st.secrets["email"]["password"]

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Tax Questionnaire PDF"

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