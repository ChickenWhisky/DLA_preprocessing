import os
import requests
import json
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from utilities import get_pdf_name
from PIL import Image, ImageDraw


# Ensure directories exist
img_dir = 'img'
table_img_dir = 'table_images'
os.makedirs(img_dir, exist_ok=True)
os.makedirs(table_img_dir, exist_ok=True)

backend_url = 'https://04d4-34-125-232-117.ngrok-free.app/predict'
tabnet_url = 'https://925f-34-138-177-111.ngrok-free.app/predict'

# Define Header, Footer, and Table classes
class Header:
    def __init__(self, text=""):
        self.text = text


class Footer:
    def __init__(self, text=""):
        self.text = text


class Table:
    def __init__(self, bbox=None):
        self.bbox = bbox or []



def detect_header_footer(image_path, footer=False):
    """
    Sends an image to the backend model for header or footer detection.
    """
    try:
        with open(image_path, 'rb') as img_file:
            response = requests.post(
                backend_url,
                files={"image": img_file},
                data={"question": "Fetch only header elements distinctly from the image" if not footer else "Fetch only footer elements distinctly from the image"}
            )

        if response.status_code == 200:
            result = response.json().get('response', "")
            return Header(text=result).__dict__
        else:
            print(f"Error processing {image_path}: {response.text}")
            return Header().__dict__

    except Exception as e:
        print(f"Exception while processing {image_path}: {str(e)}")
        return Header().__dict__


def detect_tables(image_path):
    """
    Sends an image to the backend model for table detection and visualizes the detected bounding boxes.
    """
    try:
        # Send the image to the backend for detection
        with open(image_path, 'rb') as img_file:
            response = requests.post(
                tabnet_url,
                files={"image": img_file},
            )

        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            detections = response_data.get('detections', [])

            if not detections:
                print(f"No tables detected in {image_path}")
                return [], None

            # Open the original image
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            # Draw bounding boxes
            for detection in detections:
                bbox = detection["bbox"]  # [x_min, y_min, x_max, y_max]
                draw.rectangle(bbox, outline="red", width=3)

            return detections, image

        else:
            print(f"Error processing {image_path}: {response.text}")
            return [], None

    except Exception as e:
        print(f"Exception while processing {image_path}: {str(e)}")
        return [], None


def process_pdf(pdf_path, results_file):
    """
    Converts a single PDF to high-resolution images, applies header, footer, and table detection, 
    and updates the results in the JSON file after processing each page.
    """
    print(f"Processing {pdf_path}...")

    # Convert PDF to images with high DPI for better resolution
    pdf_name = get_pdf_name(pdf_path)
    images = convert_from_path(pdf_path, dpi=300)  # Set DPI to 300 for high resolution

    for image_index, image in enumerate(images):
        page_number = image_index + 1
        image_path = os.path.join(img_dir, f'{pdf_name}_{page_number}.png')
        image.save(image_path, 'PNG')

        print(f"Converted {pdf_path} page {page_number} to high-resolution image at {image_path}.")

        # Initialize results for this page
        page_data = {
            "header": None,
            "footer": None,
            "tables": []
        }

        # Detect header and footer
        page_data["header"] = detect_header_footer(image_path)
        page_data["footer"] = detect_header_footer(image_path, footer=True)

        # Detect tables and optionally save table images
        tables, table_detected_image = detect_tables(image_path)
        page_data["tables"] = [Table(bbox=t["bbox"]).__dict__ for t in tables]

        # Save table-detected image if tables are found
        if tables:
            table_image_path = os.path.join(table_img_dir, f'{pdf_name}_page_{page_number}_tables.png')
            table_detected_image.save(table_image_path, 'PNG')

        # Load the current results file
        try:
            if os.path.exists(results_file):
                with open(results_file, "r") as json_file:
                    results = json.load(json_file)
            else:
                results = {}
        except Exception as e:
            print(f"Error loading results file: {e}")
            results = {}

        # Update the results with the current page data
        if pdf_name not in results:
            results[pdf_name] = {}
        results[pdf_name][page_number] = page_data

        # Save the updated results to the JSON file
        try:
            with open(results_file, "w") as json_file:
                json.dump(results, json_file, indent=4)
            print(f"Results for page {page_number} updated in {results_file}.")
        except Exception as e:
            print(f"Error saving results file: {e}")


def process_pdfs_concurrently(pdf_directory):
    """
    Processes multiple PDFs in the given directory concurrently and updates results after each page.
    """
    results_file = "results.json"
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda pdf: process_pdf(pdf, results_file), pdf_files)

def main():
    process_pdfs_concurrently('./amazon_ocr_samples/single_col/test/')


if __name__ == "__main__":
    main()
