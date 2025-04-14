import json
from datetime import datetime, timedelta

# Get today's date in GMT+7 timezone
now = datetime.utcnow() + timedelta(hours=7)
today_date = now.strftime("%Y-%m-%d")

print(f"Creating a dynamic date solution for {today_date} (GMT+7)")

# Update the main notebook to inject the current date into the Upload_image.ipynb at runtime
with open('SDVN_ComfyUI_Flux_v3.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Modify the second cell (index 1) to use dynamic date approach
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
    'import os, re\n',
    '\n',
    '# Define a function to run the upload script in a separate thread\n',
    'def run_upload_script():\n',
    '    import time\n',
    '    # Give ComfyUI a moment to start up\n',
    '    time.sleep(10)\n',
    '    print("\\n\\033[1;32mStarting Upload_image.ipynb for model management...\\033[0m")\n',
    '    \n',
    '    # Get today\'s date in GMT+7 timezone\n',
    '    now = datetime.utcnow() + timedelta(hours=7)  # GMT+7\n',
    '    today = now.strftime("%Y-%m-%d")\n',
    '    print(f"\\033[1;32mImages will be saved to folder: {today} (GMT+7 timezone)\\033[0m")\n',
    '    \n',
    '    # Create a dynamic version of Upload_image.ipynb with current date\n',
    '    # First, dynamically create the current date folder\n',
    '    todays_folder = f"/content/drive/MyDrive/SD-Data/Export/ComfyUI/{today}/"\n',
    '    os.makedirs(todays_folder, exist_ok=True)\n',
    '    \n',
    '    # Create a dynamic modified version of Upload_image.ipynb with today\'s date\n',
    '    src_path = "/content/SDVN-WebUI/Upload_image.ipynb"\n',
    '    dst_path = "/tmp/dynamic_upload_image.ipynb"\n',
    '    \n',
    '    # Read the original file\n',
    '    with open(src_path, "r", encoding="utf-8") as f:\n',
    '        content = f.read()\n',
    '    \n',
    '    # Replace the hardcoded date with today\'s date\n',
    '    content = re.sub(\n',
    '        r\'DEFAULT_UPLOAD_FOLDER = \\\'/content/drive/MyDrive/SD-Data/Export/ComfyUI/[^/]*\\\'\',\n',
    '        f\'DEFAULT_UPLOAD_FOLDER = \\\'/content/drive/MyDrive/SD-Data/Export/ComfyUI/{today}/\\\'\',\n',
    '        content\n',
    '    )\n',
    '    content = re.sub(\n',
    '        r\'\\.replace\\(\\\'/content/drive/MyDrive/SD-Data/Export/ComfyUI/[^/]*/\\\'\',\n',
    '        f\'.replace(\\\'/content/drive/MyDrive/SD-Data/Export/ComfyUI/{today}/\\\'\',\n',
    '        content\n',
    '    )\n',
    '    \n',
    '    # Write the modified file\n',
    '    with open(dst_path, "w", encoding="utf-8") as f:\n',
    '        f.write(content)\n',
    '    \n',
    '    print(f"Created dynamic version of Upload_image.ipynb with current date: {today}")\n',
    '    \n',
    '    # Run the modified version\n',
    '    %run /tmp/dynamic_upload_image.ipynb\n',
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

print('SDVN_ComfyUI_Flux_v3.ipynb updated with dynamic date functionality!') 