import os
import requests
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from utilities import get_pdf_name

# Ensure img directory exists
img_dir = 'img'
os.makedirs(img_dir, exist_ok=True)

backend_url = 'https://04d4-34-125-232-117.ngrok-free.app/predict'

def process_pdf(pdf_path):
    """
    Converts a single PDF to high-resolution images, applies a function, and checks for header and footer.
    """
    print(f"Processing {pdf_path}...")

    # Convert PDF to images with high DPI for better resolution
    pdf_name = get_pdf_name(pdf_path)
    images = convert_from_path(pdf_path, dpi=300)  # Set DPI to 300 for high resolution
    for image_index, image in enumerate(images):
        image_path = os.path.join(img_dir, f'{pdf_name}_{image_index + 1}.png')
        image.save(image_path, 'PNG')
        print(f"Converted {pdf_path} page {image_index + 1} to high-resolution image at {image_path}.")

        # Send the image to the backend for header and footer detection
        detect_header_footer(image_path)


def detect_header_footer(image_path):
    """
    Sends an image to the backend model for header and footer detection.
    """
    try:
        with open(image_path, 'rb') as img_file:
            response = requests.post(
                backend_url,
                files={"image": img_file},
                data={"question": "Fetch only header and footer elements distinctly from the image. Give the header and footer in JSN format"}
            )

        if response.status_code == 200:
            result = response.json().get('response', "No response")
            print(f"Header/Footer in {image_path}: {result}")
        else:
            print(f"Error processing {image_path}: {response.text}")

    except Exception as e:
        print(f"Exception while processing {image_path}: {str(e)}")


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
