from PyPDF2 import PdfReader

def list_pdf_fields(pdf_path):
    """
    List all fillable PDF fields with type, current value, and tooltip/label.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        dict: Dictionary of field info
    """
    try:
        pdf = PdfReader(pdf_path)
        fields = pdf.get_fields()
        if not fields:
            print(f"No fillable fields detected in {pdf_path}.")
            return {}

        field_info = {}
        print(f"Fillable fields detected in {pdf_path}:")
        for name, info in fields.items():
            field_type = info.get('/FT') if info else 'Unknown'
            value = info.get('/V') if info else None
            tooltip = info.get('/TU') if info else None  # This may be the visible label
            field_info[name] = {
                'type': field_type,
                'value': value,
                'label': tooltip
            }
            print(f"- Field Name: {name}, Type: {field_type}, Value: {value}, Label: {tooltip}")
        
        return field_info

    except FileNotFoundError:
        print(f"Error: File not found - {pdf_path}")
        return {}
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {}

