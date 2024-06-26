from detectColumns import detect_columns


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
    image_path = pathToImage  # Replace with your image path

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
        if(columns<=2):
            left_image, right_image = split_image(original_image, line_coordinates)

            # Save the split images as L1_double.png and R1_double.png
            if left_image is not None and right_image is not None:
                cv2.imwrite('./L_double.png', left_image)
                cv2.imwrite('./R_double.png', right_image)

                print('Left and right images saved as L1_double.png and R1_double.png.')
        else:
            cv2.imwrite('./single.png',original_image)
            print('Whole image is saved as singlepng.')