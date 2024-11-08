import os
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor
from imageProcessing import applyOnImage
from utilities import get_pdf_name
#from headerfooter import headerFooter

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
        applyOnImage(image_path)
        image.save(image_path, 'PNG')
        print(f"Converted {pdf_path} page {image_index + 1} to high-resolution image at {image_path}.")
        
    # Convert PDF to high-resolution image (300 DPI) and low-resolution image (72 DPI)
    high_res_images = convert_from_path(pdf_path, dpi=300)
    low_res_images = convert_from_path(pdf_path, dpi=72)
    
    # Display the first page of both high-res and low-res images side by side
    high_res_image = high_res_images[1]
    low_res_image = low_res_images[1]
    
    # Save high and low-resolution images with specified file names
    high_res_image.save('high_res_image.png', 'PNG')
    low_res_image.save('low_res_image.png', 'PNG')

    #headerFooter(image_path)
        # Apply the function on the converted image
    

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
