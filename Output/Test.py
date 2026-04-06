from PyPDF2 import PdfReader, PdfWriter

pdf_path = "/Users/bobk/TaxProject/1040_2025.pdf"
output_path = "/Users/bobk/TaxProject/1040_2025_filled.pdf"

reader = PdfReader(pdf_path)
writer = PdfWriter()

# Copy pages
for page in reader.pages:
    writer.add_page(page)

# Set the value of the field
field_name = 'f1_09[0]'
fields_to_update = {field_name: 'alpha'}  # changed value to alpha

# Update each page individually
for page in writer.pages:
    writer.update_page_form_field_values(page, fields_to_update)

# Preserve the AcroForm so fields stay fillable
root = reader.trailer["/Root"].get_object()
acro_form = root.get("/AcroForm")
if acro_form:
    writer._root_object.update({
        "/AcroForm": acro_form
    })

# Save the updated PDF
with open(output_path, "wb") as f:
    writer.write(f)

print(f"Field {field_name} updated with 'alpha'. PDF saved to {output_path}")