import json

# Open the notebook file with UTF-8 encoding
with open('Upload_image.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Update the line with the fixed f-string format
notebook['cells'][0]['source'][509] = '    folder_name_display = app.config[\'UPLOAD_FOLDER\'].replace(f\'/content/drive/MyDrive/SD-Data/Export/ComfyUI/{current_date}/\', \'\')\n'

# Save the modified notebook with UTF-8 encoding
with open('Upload_image.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Notebook updated successfully!") 