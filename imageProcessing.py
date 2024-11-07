from coloumndetect.detectColumns import detect_columns
from utilities import get_pdf_name, extract_fields_from_filename
import cv2
import os

# Ensure the "processed" directory exists
processed_dir = 'processed'
os.makedirs(processed_dir, exist_ok=True)

def split_image(image, line_coordinates):
    if image is None:
        print("Error: No image provided.")
        return None, None

    # Sort line coordinates to get the second line (index 1)
    line_coordinates.sort(key=lambda x: x[0][0])  # Sort by x-coordinate of the first point
    second_line = line_coordinates[1]

    # Extract x-coordinate of the second line
    x_split = second_line[0][0]

    # Split the image into left and right portions
    left_image = image[:, :x_split, :]
    right_image = image[:, x_split:, :]

    return left_image, right_image

def applyOnImage(pathToImage):
    image_path = pathToImage  # Use the provided image path

    # Detect columns and get line coordinates
    columns, result_image, line_coordinates, original_image = detect_columns(image_path, save_debug_images=True, return_lines=True)

    if columns is not None:
        print(f'Number of columns detected: {columns}')
        print(f'Debug image saved to: {result_image}')
        if line_coordinates:
            print(f'Coordinates of lines between columns:')
            for line in line_coordinates:
                print(line)

        # Split the image based on the detected lines
        if columns <= 2:
            left_image, right_image = split_image(original_image, line_coordinates)

            # Save the split images
            if left_image is not None and right_image is not None:
                pdf_name, pageNumber = extract_fields_from_filename(pathToImage)
                left_image_path = os.path.join(processed_dir, f'L_{pageNumber}_{pdf_name}.png')
                right_image_path = os.path.join(processed_dir, f'R_{pageNumber}_{pdf_name}.png')
                cv2.imwrite(left_image_path, left_image)
                cv2.imwrite(right_image_path, right_image)

                print(f'Left image saved as {left_image_path}.')
                print(f'Right image saved as {right_image_path}.')
        else:
            pdf_name, pageNumber = extract_fields_from_filename(pathToImage)
            single_image_path = os.path.join(processed_dir, f'S_{pageNumber}_{pdf_name}.png')
            cv2.imwrite(single_image_path, original_image)
            print(f'Whole image is saved as {single_image_path}.')
