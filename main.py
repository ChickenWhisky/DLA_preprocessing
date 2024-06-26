
import os
import tempfile
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from imageProcessing import split_image , applyOnImage

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

def process_pdf(pdf_path):
    """
    Converts a single PDF to images and applies a function on each image.
    """
    print(f"Processing {pdf_path}...")

    # Convert PDF to images
    with tempfile.TemporaryDirectory() as temp_dir:
        images = convert_from_path(pdf_path, output_folder=temp_dir)
        for image_index, image in enumerate(images):
            image_path = os.path.join(temp_dir, f'image_{image_index}.png')
            image.save(image_path, 'PNG')
            print(f"Converted {pdf_path} page {image_index + 1} to image.")

            # Apply the function on the converted image
            applyOnImage(image_path)

def process_pdfs_concurrently(pdf_directory):
    """
    Processes multiple PDFs in the given directory concurrently.
    """
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    # Use ThreadPoolExecutor to process PDFs in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(process_pdf, pdf_files)
def main():
    process_pdfs_concurrently('./pdfs')    


if __name__=="__main__":
    main()