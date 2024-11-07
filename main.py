import os
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from imageProcessing import applyOnImage
from utilities import get_pdf_name

# Ensure img directory exists
img_dir = 'img'
os.makedirs(img_dir, exist_ok=True)

def process_pdf(pdf_path):
    """
    Converts a single PDF to high-resolution images and applies a function on each image.
    """
    print(f"Processing {pdf_path}...")

    # Convert PDF to images with high DPI for better resolution
    pdf_name = get_pdf_name(pdf_path)
    images = convert_from_path(pdf_path, dpi=300)  # Set DPI to 300 for high resolution
    for image_index, image in enumerate(images):
        image_path = os.path.join(img_dir, f'{pdf_name}_{image_index}.png')
        image.save(image_path, 'PNG')
        print(f"Converted {pdf_path} page {image_index + 1} to high-resolution image at {image_path}.")

        # Apply the function on the converted image
        #applyOnImage(image_path)

def process_pdfs_concurrently(pdf_directory):
    """
    Processes multiple PDFs in the given directory concurrently.
    """
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    with ThreadPoolExecutor() as executor:
        executor.map(process_pdf, pdf_files)

def main():
    process_pdfs_concurrently('./amazon_ocr_samples/single_col/test/')

if __name__ == "__main__":
    main()
