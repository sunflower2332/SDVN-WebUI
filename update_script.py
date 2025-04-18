# Script to update Upload_image.ipynb for dynamic GMT+7 folder paths

"""
Follow these steps to update your Upload_image.ipynb file to use dynamic GMT+7 date folders
and add batch download functionality:

1. Install the pytz package and zipfile
   Add to your pip install command:
   !pip install -q flask nest_asyncio unidecode flask-limiter pytz

2. Import pytz and zipfile in your imports section:
   import pytz
   import zipfile
   import io

3. Replace the fixed DEFAULT_UPLOAD_FOLDER with dynamic date:
   # Get current date in GMT+7 (Bangkok timezone)
   gmt7 = pytz.timezone('Asia/Bangkok')
   current_date = datetime.now(gmt7).strftime('%Y-%m-%d')
   
   # Default upload folder in Google Drive using current date
   DEFAULT_UPLOAD_FOLDER = f'/content/drive/MyDrive/SD-Data/Export/ComfyUI/{current_date}/'

4. Add these new routes to your file for batch downloads:

@app.route('/download_all')
def download_all_files():
    # Create a BytesIO object to store the zip file
    memory_file = io.BytesIO()
    
    try:
        # Create a zip file in memory
        with zipfile.ZipFile(memory_file, 'w') as zf:
            if os.path.exists(app.config['UPLOAD_FOLDER']):
                for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                        zf.write(file_path, arcname=filename)
        
        # Seek to the beginning of the file
        memory_file.seek(0)
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_folder = os.path.basename(os.path.normpath(app.config['UPLOAD_FOLDER']))
        
        # Send the file as a response
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'images_{current_folder}_{timestamp}.zip'
        )
    except Exception as e:
        return redirect(url_for('index', error=f"Error downloading files: {str(e)}"))

@app.route('/download_selected', methods=['POST'])
def download_selected_files():
    # Create a BytesIO object to store the zip file
    memory_file = io.BytesIO()
    
    try:
        # Get the list of selected files
        selected_files = request.form.getlist('selected_files')
        
        if not selected_files:
            return redirect(url_for('index', error="No files selected for download"))
        
        # Create a zip file in memory
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for filename in selected_files:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(file_path):
                    zf.write(file_path, arcname=filename)
        
        # Seek to the beginning of the file
        memory_file.seek(0)
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Send the file as a response
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'selected_images_{timestamp}.zip'
        )
    except Exception as e:
        return redirect(url_for('index', error=f"Error downloading files: {str(e)}"))

5. Don't forget to add the import for send_file:
   from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory, jsonify, send_file

6. COPY-PASTE FRIENDLY HTML TEMPLATE CHANGES:
   Look for the HTML_TEMPLATE variable in your notebook and make these changes:

   A) Add this CSS inside the <style> section:
   
```css
.btn-download {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    text-decoration: none;
    display: inline-block;
}
.btn-download:hover {
    background-color: #218838;
}
.btn-small {
    padding: 4px 8px;
    font-size: 12px;
}
```

   B) Find the header-actions div section and replace it with:
   
```html
<div class="header-actions">
    <button onclick="window.location.href='/?page={{ current_page }}'" class="refresh-btn">Refresh</button>
    {% if files %}
    <a href="/delete_all" class="btn btn-delete" onclick="return confirm('Bạn có chắc muốn xóa TẤT CẢ ảnh trong thư mục này?')">Delete All Photos</a>
    <a href="/download_all" class="btn btn-download">Download All Photos</a>
    {% endif %}
</div>
```

   C) Find the batch-actions div section and replace it with:
   
```html
<div class="batch-actions">
    <button type="button" onclick="selectAll()" class="btn">Select All</button>
    <button type="button" onclick="deselectAll()" class="btn">Deselect All</button>
    <button type="submit" class="btn btn-delete" onclick="return confirmDelete()">Delete Selected</button>
    <button type="button" onclick="downloadSelected()" class="btn btn-download">Download Selected</button>
</div>
```

   D) Add this JavaScript function before the closing </script> tag:
   
```javascript
function downloadSelected() {
    const checkboxes = document.querySelectorAll('input[name="selected_files"]:checked');
    if (checkboxes.length === 0) {
        alert('No files selected!');
        return false;
    }
    
    // Create a form and submit it
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/download_selected';
    
    // Copy all selected checkboxes to the form
    checkboxes.forEach(checkbox => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_files';
        input.value = checkbox.value;
        form.appendChild(input);
    });
    
    // Add the form to the body, submit it, and then remove it
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}
```

   E) You can also add a download button for each individual image in the file-actions div:
   
```html
<div class="file-actions">
    <a href="/download/{{ file.name }}" class="btn btn-small">Download</a>
    <a href="/delete/{{ file.name }}?page={{ current_page }}" class="btn btn-delete btn-small" onclick="return confirm('Bruh có chắc muốn xóa ảnh này?')">Delete</a>
    <a href="#" onclick="downloadSingle('{{ file.name }}'); return false;" class="btn btn-download btn-small">Zip</a>
</div>
```
   
   F) Add this JavaScript function for individual image download:
   
```javascript
function downloadSingle(filename) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/download_selected';
    
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'selected_files';
    input.value = filename;
    form.appendChild(input);
    
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}
```

7. Update the setup_photo_uploader function to refresh the folder on each run:
   # Inside setup_photo_uploader function
   # Update folder with current date in GMT+7
   global DEFAULT_UPLOAD_FOLDER
   gmt7 = pytz.timezone('Asia/Bangkok')
   current_date = datetime.now(gmt7).strftime('%Y-%m-%d')
   DEFAULT_UPLOAD_FOLDER = f'/content/drive/MyDrive/SD-Data/Export/ComfyUI/{current_date}/'
   app.config['UPLOAD_FOLDER'] = DEFAULT_UPLOAD_FOLDER
"""
