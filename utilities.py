import os

def get_pdf_name(pdf_path):
    """
    Extracts the name of a PDF file from its path.

    Parameters:
    - pdf_path (str): The full path to the PDF file.

    Returns:
    - str: The name of the PDF file without its extension.
    """
    # Check if the path is valid and points to a PDF file
    if not os.path.exists(pdf_path) or not pdf_path.endswith('.pdf'):
        print("Invalid PDF path or file does not exist.")
        return None

    # Extract the base name of the file (including extension)
    pdf_basename = os.path.basename(pdf_path)

    # Remove the '.pdf' extension to get just the name
    pdf_name = os.path.splitext(pdf_basename)[0]

    return pdf_name