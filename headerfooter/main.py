from transformers import CLIPProcessor, AutoModel
from PIL import Image
import os

# Path to your image
image_path = os.path.join("../img/8_7973018_0.png")

def headerfooter(image_path):
    # Load the model and processor
    model = AutoModel.from_pretrained("OpenGVLab/InternVL2-1B", trust_remote_code=True)
    processor = CLIPProcessor.from_pretrained("OpenGVLab/InternVL2-1B", trust_remote_code=True)

    # Load image
    image = Image.open(image_path)

    # Prepare inputs (image and prompt for extraction)
    inputs = processor(images=image, text="Extract header and footer", return_tensors="pt")

    # Forward pass through the model
    outputs = model(**inputs)

    # Check the model output to understand its structure
    print("Model Output:", outputs)

    # Attempt to extract header and footer (adjust based on model output)
    try:
        # Assuming the output contains 'header' and 'footer' keys (this may vary)
        header_region = outputs.get("header", None)
        footer_region = outputs.get("footer", None)

        if header_region is not None and footer_region is not None:
            print("Header Region:", header_region)
            print("Footer Region:", footer_region)
        else:
            print("Header/Footer not found in the model output.")
    except Exception as e:
        print(f"Error extracting header/footer: {e}")

# Run the function
headerfooter(image_path)
