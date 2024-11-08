import camelot

# Load the PDF file
tables = camelot.read_pdf('../amazon_ocr_samples/single_col/8_7973018.pdf', pages='1', flavor='stream')

# Check the number of tables detected
print(f"Number of tables detected: {len(tables)}")

# Print the first table (as a DataFrame)
print(tables[0].df)

# Optionally, export to CSV or Excel
tables[0].to_csv('output.csv')
tables[0].to_excel('output.xlsx')
