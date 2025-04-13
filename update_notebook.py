import json

# Read the original notebook
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
    '\n',
    '# Define a function to run the upload script in a separate thread\n',
    'def run_upload_script():\n',
    '    import time\n',
    '    # Give ComfyUI a moment to start up\n',
    '    time.sleep(10)\n',
    '    print("\\n\\033[1;32mStarting Upload_image.ipynb for model management...\\033[0m")\n',
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

print('Notebook updated successfully!') 