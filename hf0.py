import fitz  # PyMuPDF
import cv2
import numpy as np

def convert_pdf_to_images(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    images = []
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:  # RGBA
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        images.append(img.copy())  # Make a writable copy of the image array
    
    return images

def detect_headers_and_footers(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding to get a binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Find horizontal and vertical projections
    vertical_projection = np.sum(binary, axis=1)
    
    # Identify regions with text
    threshold = np.max(vertical_projection) * 0.1
    text_regions = vertical_projection > threshold
    
    # Determine boundaries of text regions
    region_boundaries = []
    in_region = False
    for i, has_text in enumerate(text_regions):
        if has_text and not in_region:
            start = i
            in_region = True
        elif not has_text and in_region:
            end = i
            region_boundaries.append((start, end))
            in_region = False
    if in_region:
        region_boundaries.append((start, len(text_regions)))
    
    # Identify header and footer based on the positions of the regions
    header = None
    footer = None
    height, width = gray.shape
    
    if region_boundaries:
        # Header is the first region if it starts near the top
        if region_boundaries[0][0] < height * 0.3:
            header_start, header_end = region_boundaries[0]
            header = gray[header_start:header_end, :]
            cv2.rectangle(image, (0, header_start), (width, header_end), (0, 255, 0), 2)
        
        # Footer is the last region if it ends near the bottom
        if region_boundaries[-1][1] > height * 0.8:
            footer_start, footer_end = region_boundaries[-1]
            footer = gray[footer_start:footer_end, :]
            cv2.rectangle(image, (0, footer_start), (width, footer_end), (0, 0, 255), 2)
    
    return image, header, footer

def process_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    processed_images = []
    for image in images:
        processed_image, header, footer = detect_headers_and_footers(image)
        processed_images.append(processed_image)
        # Optionally, save or display headers and footers
        if header is not None:
            cv2.imwrite("header.png", header)
        if footer is not None:
            cv2.imwrite("footer.png", footer)
    return processed_images

# Example usage
pdf_path = 'single.pdf'
processed_images = process_pdf(pdf_path)

# Display processed images
for img in processed_images:
    cv2.imshow('Processed Image', img)
    cv2.waitKey(0)
cv2.destroyAllWindows()
