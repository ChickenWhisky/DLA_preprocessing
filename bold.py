import cv2
import numpy as np

# Load the image
image = cv2.imread('./img/8_7973018_0.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to detect text regions
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

# Apply morphological operations to highlight bold text regions
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=2)

# Find contours in the dilated image
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Visualize bold text regions based on contour properties
for cnt in contours:
    # Get the bounding box for each contour
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Filter out small contours and check if the aspect ratio is suitable
    aspect_ratio = w / float(h)
    if w > 20 and h > 10 and aspect_ratio < 3:  # You can adjust these values
        # Draw the bounding box around the bold text
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Show the final result with bold text regions highlighted
cv2.imshow('Bold Text Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
