import json
import re
from datetime import datetime, timedelta

# Get today's date in GMT+7 timezone
now = datetime.utcnow() + timedelta(hours=7)
today_date = now.strftime("%Y-%m-%d")

print(f"Setting upload folder date to today ({today_date}) in GMT+7 timezone")

# 1. First update the Upload_image.ipynb file
try:
    with open('Upload_image.ipynb', 'r', encoding='utf-8') as f:
        upload_notebook = json.load(f)
    
    # Find the cell with the DEFAULT_UPLOAD_FOLDER variable
    for cell_index, cell in enumerate(upload_notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
            
        source = ''.join(cell['source'])
        if 'DEFAULT_UPLOAD_FOLDER =' in source:
            # Replace the hardcoded date with today's date
            new_source = []
            for line in cell['source']:
                if 'DEFAULT_UPLOAD_FOLDER =' in line:
                    # Extract the path pattern and replace only the date part
                    pattern = r"DEFAULT_UPLOAD_FOLDER = '(/content/drive/MyDrive/SD-Data/Export/ComfyUI/).*?/'"
                    match = re.search(pattern, line)
                    if match:
                        base_path = match.group(1)
                        updated_line = f"DEFAULT_UPLOAD_FOLDER = '{base_path}{today_date}/'\n"
                        new_source.append(updated_line)
                    else:
                        # If pattern doesn't match, keep the original line
                        new_source.append(line)
                else:
                    new_source.append(line)
            
            # Update the cell source
            upload_notebook['cells'][cell_index]['source'] = new_source
            print(f"Updated DEFAULT_UPLOAD_FOLDER in cell {cell_index}")
            
        # Also find and update the folder_name_display line
        if 'folder_name_display =' in source and '.replace(' in source:
            new_source = []
            for line in cell['source']:
                if 'folder_name_display =' in line and '.replace(' in line:
                    # Replace the path pattern in the replace() function
                    pattern = r"\.replace\('(/content/drive/MyDrive/SD-Data/Export/ComfyUI/).*?/'"
                    match = re.search(pattern, line)
                    if match:
                        base_path = match.group(1)
                        updated_line = line.replace(match.group(0), f".replace('{base_path}{today_date}/'")
                        new_source.append(updated_line)
                    else:
                        new_source.append(line)
                else:
                    new_source.append(line)
                    
            # Update the cell source
            upload_notebook['cells'][cell_index]['source'] = new_source
            print(f"Updated folder_name_display in cell {cell_index}")
    
    # Write the updated Upload_image.ipynb file
    with open('Upload_image.ipynb', 'w', encoding='utf-8') as f:
        json.dump(upload_notebook, f, ensure_ascii=False, indent=1)
    
    print(f"Upload_image.ipynb updated with today's date: {today_date}")
except Exception as e:
    print(f"Error updating Upload_image.ipynb: {str(e)}")

# 2. Now update the main notebook as before
with open('SDVN_ComfyUI_Flux_v3.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Modify the second cell (index 1) to add an option to run either the main workflow or upload script
cell = notebook['cells'][1]
source = cell['source']
new_source = [
    '#@title # ⌛️ 2.RUN\n',
    'RunMode = "Run ComfyUI" #@param ["Run ComfyUI", "Upload Models", "Run Both (ComfyUI First)"]\n',
    'DriveLib = True\n',
    'CommandLine = "" #@param {type:"string"}\n',
    '\n',
    'if RunMode == "Upload Models":\n',
    '    print("\\n\\033[1;32mRunning Upload_image.ipynb for model management...\\033[0m")\n',
    '    %run /content/SDVN-WebUI/Upload_image.ipynb\n',
    'elif RunMode == "Run ComfyUI" or RunMode == "Run Both (ComfyUI First)":\n',
    '    install_custom()\n',
    '    import time\n',
    '    run_ver(Version,CommandLine)\n',
    '    \n',
    '    if RunMode == "Run Both (ComfyUI First)":\n',
    '        print("\\n\\033[1;33mComfyUI is now running. To use Upload_image.ipynb, either:\\033[0m")\n',
    '        print("\\033[1;33m1. Stop this cell and select \'Upload Models\' from the dropdown, or\\033[0m")\n',
    '        print("\\033[1;33m2. Open Upload_image.ipynb in a new tab: https://colab.research.google.com/github/sunflower2332/SDVN-WebUI/blob/main/Upload_image.ipynb\\033[0m")\n'
]
notebook['cells'][1]['source'] = new_source

# Write the modified notebook
with open('SDVN_ComfyUI_Flux_v3.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print('Notebook updated successfully!')