import json

# Read the Upload_image.ipynb file
with open('Upload_image.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the cell that contains the Flask app configuration
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if "app = Flask(__name__)" in source and "MAX_CONTENT_LENGTH" in source:
            # Find the line with MAX_CONTENT_LENGTH and modify it
            for i, line in enumerate(cell['source']):
                if "app.config['MAX_CONTENT_LENGTH']" in line:
                    # Replace 16MB with 64MB
                    cell['source'][i] = line.replace("16 * 1024 * 1024", "64 * 1024 * 1024").replace("16MB", "64MB")
                    print(f"Updated MAX_CONTENT_LENGTH from 16MB to 64MB")
                    break

# Write the modified notebook back to the file
with open('Upload_image.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Upload_image.ipynb has been updated to allow file uploads up to 64MB") 