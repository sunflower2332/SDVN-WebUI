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

# Modify the second cell (index 1) to run both simultaneously
cell = notebook['cells'][1]
source = cell['source']
new_source = [
    '#@title # ⌛️ 2.RUN\n',
    'DriveLib = True\n',
    'RunModels = True #@param {type:"boolean"}\n',
    'CommandLine = "" #@param {type:"string"}\n',
    'install_custom()\n',
    'import time\n',
    'import threading\n',
    'from datetime import datetime, timedelta\n',
    '\n',
    '# Define a function to run the upload script in a separate thread\n',
    'def run_upload_script():\n',
    '    import time\n',
    '    # Give ComfyUI a moment to start up\n',
    '    time.sleep(10)\n',
    '    print("\\n\\033[1;32mStarting Upload_image.ipynb for model management...\\033[0m")\n',
    '    # Ensure Upload_image.ipynb uses today\'s date\n',
    '    now = datetime.utcnow() + timedelta(hours=7) # GMT+7\n',
    '    today = now.strftime("%Y-%m-%d")\n',
    '    print(f"\\033[1;32mImages will be saved to folder: {today} (GMT+7 timezone)\\033[0m")\n',
    '    # Run the upload script\n',
    '    %run /content/SDVN-WebUI/Upload_image.ipynb\n',
    '\n',
    '# Start the upload script in a separate thread if enabled\n',
    'if RunModels:\n',
    '    thread = threading.Thread(target=run_upload_script)\n',
    '    thread.daemon = True\n',
    '    thread.start()\n',
    '    print("\\033[1;33mModel uploader will start shortly in the background...\\033[0m")\n',
    '\n',
    '# Run ComfyUI\n',
    'run_ver(Version, CommandLine)\n'
]
notebook['cells'][1]['source'] = new_source

# Write the modified notebook
with open('SDVN_ComfyUI_Flux_v3.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print('SDVN_ComfyUI_Flux_v3.ipynb updated successfully!') 