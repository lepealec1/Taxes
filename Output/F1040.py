from PyPDF2 import PdfReader

def run_f1040(pdf_path):
    """
    Load a PDF and return all fillable AcroForm fields.
    Args:
        pdf_path (str): Path to the PDF file
    Returns:
        dict: Dictionary of field names and simplified info, empty if none
    """
    try:
        pdf = PdfReader(pdf_path)
        fields = pdf.get_fields()
        if not fields:
         #   print(f"No fillable fields detected in {pdf_path}.")
            return {}

        clean_fields = {}
#        print(f"Fillable fields detected in {pdf_path}:")
        for name, info in fields.items():
            field_type = info.get('/FT') if info else 'Unknown'
            clean_fields[name] = {'type': field_type}
         #   print(f"- {name} ({field_type})")
        
        return clean_fields
    except FileNotFoundError:
        print(f"Error: File not found - {pdf_path}")
        return {}
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {}