"""
This is a fixed HTML template for the Upload_image.ipynb file.

To use it:
1. Copy the HTML_TEMPLATE variable below
2. Paste it into your Upload_image.ipynb file, replacing the existing HTML_TEMPLATE variable
3. Add the following routes to your file:

# At the top of your file, import these modules
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import time
import glob
import threading
import subprocess
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app with high upload limit
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DEFAULT_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64MB limit
app.config['MAX_CONTENT_PATH'] = None  # Disable path limit

# Error handlers to prevent crashes
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    # Return to the main page with error message
    return redirect(url_for('index', error=f"An error occurred: {str(e)}"))

@app.route('/delete_all')
def delete_all_files():
    page = request.args.get('page', 1, type=int)
    try:
        deleted_count = 0
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    os.remove(file_path)
                    deleted_count += 1
        
        message = f"Deleted {deleted_count} file(s) successfully"
        return redirect(url_for('index', message=message, page=page))
    except Exception as e:
        logger.error(f"Error deleting files: {str(e)}", exc_info=True)
        error = f"Error deleting files: {str(e)}"
        return redirect(url_for('index', error=error, page=page))

@app.route('/delete_selected', methods=['POST'])
def delete_selected_files():
    page = request.args.get('page', 1, type=int)
    try:
        selected_files = request.form.getlist('selected_files')
        deleted_count = 0
        
        for filename in selected_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1
        
        message = f"Deleted {deleted_count} file(s) successfully"
        return redirect(url_for('index', message=message, page=page))
    except Exception as e:
        logger.error(f"Error deleting selected files: {str(e)}", exc_info=True)
        error = f"Error deleting files: {str(e)}"
        return redirect(url_for('index', error=error, page=page))

# Modify your upload route to handle large files gracefully
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return redirect(url_for('index', error="No file part"))

        files = request.files.getlist('file')

        if not files or files[0].filename == '':
            return redirect(url_for('index', error="No files selected"))

        upload_count = 0
        errors = []

        for file in files:
            if file and file.filename:
                try:
                    # Create timestamped filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = secure_filename(file.filename)
                    base, ext = os.path.splitext(filename)
                    new_filename = f"{timestamp}_{base}{ext}"

                    # Save the file
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                    file.save(file_path)
                    upload_count += 1
                except Exception as e:
                    logger.error(f"Error uploading {file.filename}: {str(e)}", exc_info=True)
                    errors.append(f"Error uploading {file.filename}: {str(e)}")

        if errors:
            return redirect(url_for('index', error="; ".join(errors)))
        else:
            message = f"Successfully uploaded {upload_count} file(s)"
            return redirect(url_for('index', message=message))
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return redirect(url_for('index', error=f"Upload error: {str(e)}"))

# Also update your tunnelto_thread function to be more resilient:
def tunnelto_thread(port, api):
    import socket
    
    # Wait for the Flask app to start
    retry_count = 0
    max_retries = 15
    while retry_count < max_retries:
        time.sleep(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                break
        except Exception:
            pass
        finally:
            sock.close()
        retry_count += 1
        print(f"Waiting for Flask app to start... {retry_count}/{max_retries}")
    
    if retry_count >= max_retries:
        print("Failed to connect to Flask app. Please check if it's running.")
        return None
    
    # Set the auth key
    try:
        cmd = ["/root/.tunnelto/bin/tunnelto", "set-auth", "--key", api[0]]
        subprocess.run(cmd, timeout=30)
        
        # Start the tunnel with increased timeouts
        cmd_run = ["/root/.tunnelto/bin/tunnelto", "--subdomain", api[1], "--port", f"{port}"]
        process = subprocess.Popen(cmd_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        
        # Display the tunnel URL
        print(f"\\033[92m{'🔗 Link online để sử dụng:'}\\033[0m", f"https://{api[1]}.tunn.dev")
        
        # Display additional information
        print("\\n============================================================")
        print(f"Photo Uploader is running at: https://{api[1]}.tunn.dev")
        print("This URL can be accessed from any device with internet access")
        print("Upload folder:", app.config['UPLOAD_FOLDER'])
        print("Maximum upload size: 64MB")
        print("============================================================\\n")
        
        return process
    except Exception as e:
        logger.error(f"Error setting up tunnel: {str(e)}", exc_info=True)
        print(f"Error setting up tunnel: {str(e)}")
        return None
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Photo Uploader</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f7f9fc;
        }
        h1, h2 {
            color: #333;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .file-list {
            background-color: #f7f7f7;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .files-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        .file-item {
            display: flex;
            flex-direction: column;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
        }
        .file-checkbox {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 10;
            transform: scale(1.5);
            opacity: 0.8;
        }
        .file-actions {
            display: flex;
            justify-content: space-between;
            gap: 5px;
            padding: 8px;
            background-color: #f9f9f9;
        }
        .upload-form {
            margin: 20px 0;
        }
        input[type="text"], input[type="file"] {
            margin-bottom: 10px;
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button, .btn {
            background-color: #4285f4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            display: inline-block;
        }
        button:hover, .btn:hover {
            background-color: #3367d6;
        }
        .btn-small {
            padding: 4px 8px;
            font-size: 12px;
        }
        .btn-delete {
            background-color: #e53935;
        }
        .btn-delete:hover {
            background-color: #c62828;
        }
        .success-message {
            color: #28a745;
            margin-bottom: 15px;
        }
        .error-message {
            color: #dc3545;
            margin-bottom: 15px;
        }
        .folder-name {
            font-weight: bold;
            margin-bottom: 15px;
            word-break: break-all;
        }
        .download-link {
            color: white;
            text-decoration: none;
        }
        .file-info {
            padding: 8px;
            word-break: break-all;
            font-size: 12px;
        }
        .thumbnail-container {
            position: relative;
            width: 100%;
            height: 300px;
            cursor: pointer;
        }
        .file-thumbnail {
            width: 100%;
            height: 100%;
            object-fit: contain;
            background-color: #f0f0f0;
        }
        .refresh-btn {
            margin-left: 10px;
            padding: 4px 8px;
            font-size: 12px;
        }
        .pagination {
            display: flex;
            justify-content: center;
            margin-top: 15px;
            gap: 5px;
        }
        .pagination button {
            min-width: 30px;
        }
        .current-page {
            background-color: #1a73e8;
        }
        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        .batch-actions {
            margin-top: 10px;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        /* Modal/Lightbox styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            padding-top: 50px;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.9);
        }
        .modal-content {
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90%;
        }
        .close {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
        }
        .close:hover,
        .close:focus {
            color: #bbb;
            text-decoration: none;
        }
        @media (max-width: 1000px) {
            .files-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        @media (max-width: 768px) {
            .files-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 480px) {
            .files-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload ảnh cho Comfy</h1>

        <div class="folder-name">
            Current folder: {{ folder_name }}
        </div>

        {% if success_message %}
        <div class="success-message">
            {{ success_message }}
        </div>
        {% endif %}

        {% if error_message %}
        <div class="error-message">
            {{ error_message }}
        </div>
        {% endif %}

        <form action="/set_folder" method="post" class="upload-form">
            <h2>Change Folder</h2>
            <input type="text" name="folder_name" placeholder="Enter folder name (Vietnamese supported)" value="{{ folder_name }}" required>
            <button type="submit">Set Folder</button>
            <p>Mn chọn nhập tên Folder (trong trường hợp trên drive chưa có Folder sẽ tự tạo folder mới), sau có Click Set Folder<p>
        </form>

        <form action="/upload" method="post" enctype="multipart/form-data" class="upload-form">
            <h2>Upload Photos</h2>
            <input type="file" name="file" multiple accept="image/*" required>
            <button type="submit">Upload</button>
        </form>
        <p>Mọi người upload thì giữ Ctrl + Chọn ảnh để có thể chọn được nhiều ảnh cùng 1 lúc, chọn Upload. <strong>Có thể tải lên tới 64MB mỗi lần.</strong><p>
    </div>

    <div class="container">
        <h2>
            Uploaded Files
        </h2>
        <div class="header-actions">
            <button onclick="window.location.href='/?page={{ current_page }}'" class="refresh-btn">Refresh</button>
            {% if files %}
            <a href="/delete_all" class="btn btn-delete" onclick="return confirm('Bạn có chắc muốn xóa TẤT CẢ ảnh trong thư mục này?')">Delete All Photos</a>
            {% endif %}
        </div>
        
        {% if files %}
        <form id="batch-form" action="/delete_selected" method="post">
            <div class="batch-actions">
                <button type="button" onclick="selectAll()" class="btn">Select All</button>
                <button type="button" onclick="deselectAll()" class="btn">Deselect All</button>
                <button type="submit" class="btn btn-delete" onclick="return confirmDelete()">Delete Selected</button>
            </div>
            
            <div class="file-list">
                <div class="files-grid">
                    {% for file in files %}
                    <div class="file-item">
                        <input type="checkbox" name="selected_files" value="{{ file.name }}" class="file-checkbox">
                        <div class="thumbnail-container" onclick="openModal('{{ file.name }}')">
                            <img src="/thumbnail/{{ file.name }}" class="file-thumbnail" alt="Thumbnail">
                        </div>
                        <div class="file-info">{{ file.name }} ({{ file.size }})<br>{{ file.date }}</div>
                        <div class="file-actions">
                            <a href="/download/{{ file.name }}" class="btn btn-small">Download</a>
                            <a href="/delete/{{ file.name }}?page={{ current_page }}" class="btn btn-delete btn-small" onclick="return confirm('Bruh có chắc muốn xóa ảnh này?')">Delete</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div class="pagination">
                    {% if pages > 1 %}
                        {% if current_page > 1 %}
                            <button onclick="window.location.href='/?page={{ current_page - 1 }}'" type="button">←</button>
                        {% endif %}

                        {% for page in range(1, pages + 1) %}
                            <button onclick="window.location.href='/?page={{ page }}'" type="button" {% if page == current_page %}class="current-page"{% endif %}>{{ page }}</button>
                        {% endfor %}

                        {% if current_page < pages %}
                            <button onclick="window.location.href='/?page={{ current_page + 1 }}'" type="button">→</button>
                        {% endif %}
                    {% endif %}
                </div>
            </div>
        </form>
        {% else %}
            <div class="file-list">
                <p>No files in this folder.</p>
            </div>
        {% endif %}
        
        <p>Mn nên xóa bằng Delete trên trang này, không nên xóa trên Drive nên vì đôi lúc Drive không cập nhật sẽ bị lỗi, VD: Folder De_abc có 50 ảnh và bạn chỉ lấy 10 ảnh để Upscale bằng các xóa trên Drive nhưng vì Drive ko update kịp nên sẽ Upscale hết 50 ảnh * 2' = 100' rất tốn thời gian </p>
    </div>

    <!-- Modal for image preview -->
    <div id="imageModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImg">
    </div>

    <script>
        // Modal/Lightbox for image preview
        function openModal(imageName) {
            // Don't open modal if clicking on the checkbox
            if (event.target.type === 'checkbox') {
                return;
            }
            
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImg');
            modal.style.display = "block";
            modalImg.src = "/thumbnail/" + imageName;
            
            // Close modal when clicking outside the image
            modal.onclick = function(event) {
                if (event.target === modal || event.target.className === 'close') {
                    closeModal();
                }
            };
        }
        
        function closeModal() {
            document.getElementById('imageModal').style.display = "none";
        }
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === "Escape") {
                closeModal();
            }
        });
        
        // Batch selection functions
        function selectAll() {
            const checkboxes = document.querySelectorAll('input[name="selected_files"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = true;
            });
        }
        
        function deselectAll() {
            const checkboxes = document.querySelectorAll('input[name="selected_files"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        }
        
        function confirmDelete() {
            const checkboxes = document.querySelectorAll('input[name="selected_files"]:checked');
            if (checkboxes.length === 0) {
                alert('No files selected!');
                return false;
            }
            return confirm(`Are you sure you want to delete ${checkboxes.length} selected file(s)?`);
        }
        
        // Make thumbnail container clickable, but not when clicking the checkbox
        document.addEventListener('DOMContentLoaded', function() {
            const checkboxes = document.querySelectorAll('.file-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
        });
    </script>
</body>
</html>
''' 