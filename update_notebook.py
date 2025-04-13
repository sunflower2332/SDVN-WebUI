import json

# Read the original notebook
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
    '        print("\\033[1;33m2. Open Upload_image.ipynb in a new tab: https://colab.research.google.com/github/StableDiffusionVN/SDVN-WebUI/blob/main/Upload_image.ipynb\\033[0m")\n'
]
notebook['cells'][1]['source'] = new_source

# Write the modified notebook
with open('SDVN_ComfyUI_Flux_v3.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print('Notebook updated successfully!') 