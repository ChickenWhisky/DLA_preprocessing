import os
import matplotlib
import deepdoctection as dd
from matplotlib import pyplot as plt
from pathlib import Path

# Set the backend to 'Agg' for non-interactive plotting
matplotlib.use('Agg')

# Instantiate the analyzer
analyzer = dd.get_dd_analyzer()

# Specify the directory containing the PDFs
pdf_directory = '../../DLAPreprocessing/pdfs'
# Specify the destination folder for the output images
destination_folder = './output_pages'
os.makedirs(destination_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Iterate through all PDF files in the directory
for pdf_path in Path(pdf_directory).glob('*.pdf'):
    # Analyze the PDF
    df = analyzer.analyze(path=str(pdf_path))
    df.reset_state()

    # Process and save an image for each page
    for i, page in enumerate(df, start=1):
        image = page.viz()
        plt.figure(figsize=(25, 17))
        plt.axis('off')
        plt.imshow(image)
        # Construct the output filename {pdf_name}_{page_number}.png
        output_filename = f"{pdf_path.stem}_{i}.png"
        plt.savefig(os.path.join(destination_folder, f'page_{i}.png'), bbox_inches='tight', dpi=300)
        plt.close()