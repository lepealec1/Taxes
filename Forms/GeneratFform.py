from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(filename="supplemental_questionnaire.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, y, "Supplemental Questionnaire")

    y -= 40
    c.setFont("Helvetica", 10)

    # Name + Date
    c.drawString(40, y, "Name:")
    c.acroForm.textfield(name="name", x=90, y=y-5, width=200, height=15)

    c.drawString(350, y, "Date:")
    c.acroForm.textfield(name="date", x=390, y=y-5, width=120, height=15)

    y -= 40

    # Health Insurance
    c.drawString(40, y, "Health Insurance Coverage:")
    y -= 20

    options = ["All Year", "Part Year", "No", "Unsure"]
    x = 40
    for opt in options:
        c.drawString(x + 15, y, opt)
        c.acroForm.checkbox(name=f"hi_{opt}", x=x, y=y-5, size=12)
        x += 100

    y -= 30

    # Forms
    c.drawString(40, y, "Forms:")
    forms = ["1095-A", "1095-B", "1095-C"]
    x = 40
    y -= 20
    for f in forms:
        c.drawString(x + 15, y, f)
        c.acroForm.checkbox(name=f"form_{f}", x=x, y=y-5, size=12)
        x += 100

    y -= 30

    # Generic Yes/No/Unsure function
    def add_yes_no(label, field_name, y_pos):
        c.drawString(40, y_pos, label)
        x = 350
        for opt in ["Yes", "No", "Unsure"]:
            c.drawString(x + 15, y_pos, opt)
            c.acroForm.checkbox(name=f"{field_name}_{opt}", x=x, y=y_pos-5, size=12)
            x += 60

    # Questions
    y -= 10
    add_yes_no("Rent in CA > 6 months?", "rent_ca", y)
    y -= 25
    add_yes_no("IHSS provider?", "ihss", y)
    y -= 25
    add_yes_no("Has IP PIN?", "ippin", y)
    y -= 25
    add_yes_no("Received 1099-R?", "1099r", y)

    y -= 30

    # Text field for explanation
    c.drawString(40, y, "1099-R Explanation:")
    c.acroForm.textfield(name="1099r_explain", x=180, y=y-5, width=300, height=15)

    y -= 30

    add_yes_no("SS Lump Sum?", "ss_lump", y)
    y -= 25
    add_yes_no("Self Employment Income?", "self_emp", y)
    y -= 25
    add_yes_no("Above-the-line adjustments?", "adjustments", y)
    y -= 25
    add_yes_no("Sold stocks?", "stocks", y)
    y -= 25
    add_yes_no("Itemized deduction?", "itemized", y)
    y -= 25
    add_yes_no("Child care expenses?", "childcare", y)
    y -= 25
    add_yes_no("Received 1098-T?", "1098t", y)
    y -= 25
    add_yes_no("Estimated tax payments?", "estimated", y)

    y -= 40

    # Bank Info
    c.drawString(40, y, "Bank Name:")
    c.acroForm.textfield(name="bank_name", x=120, y=y-5, width=200, height=15)

    y -= 25

    c.drawString(40, y, "Routing Number:")
    c.acroForm.textfield(name="routing", x=140, y=y-5, width=200, height=15)

    y -= 25

    c.drawString(40, y, "Account Number:")
    c.acroForm.textfield(name="account", x=140, y=y-5, width=200, height=15)

    # Save
    c.save()
    print(f"Created {filename}")

create_pdf()