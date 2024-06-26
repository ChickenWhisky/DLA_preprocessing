import os
import shutil

def copy_and_rename_pdfs(source_dirs, target_dir):
    """
    Copies PDFs from source directories to a target directory, renaming them based on their source directory.

    Parameters:
    - source_dirs (dict): A dictionary where keys are source directory names and values are prefixes for renaming.
    - target_dir (str): The path to the directory where PDFs will be copied and renamed.
    """
    # Ensure the target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for source_dir, prefix in source_dirs.items():
        # List all PDF files in the current source directory
        pdf_files = [f for f in os.listdir(source_dir) if f.endswith('.pdf')]
        
        for index, pdf_file in enumerate(pdf_files):
            # Define the new filename based on the prefix and index
            new_filename = f"{prefix}_{index}.pdf"
            source_path = os.path.join(source_dir, pdf_file)
            target_path = os.path.join(target_dir, new_filename)
            
            # Copy and rename the PDF file
            shutil.copy(source_path, target_path)
            print(f"Copied and renamed {pdf_file} to {new_filename}")

# Define source directories and their corresponding prefixes
source_dirs = {
    '/home/thomas/Desktop/projectWithRajeshwari/Sample pdfs - Smaller/dual_column': 'd',
    '/home/thomas/Desktop/projectWithRajeshwari/Sample pdfs - Smaller/mixed_data': 'm',
    '/home/thomas/Desktop/projectWithRajeshwari/Sample pdfs - Smaller/single_column': 's',
}

# Define the target directory
target_dir = './pdfs'

# Execute the function
copy_and_rename_pdfs(source_dirs, target_dir)