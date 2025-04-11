import os
import uuid
import subprocess
import time
import re
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from threading import Thread
import locale
import shutil

# Set locale to support Vietnamese
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# HTML template for the upload page with Vietnamese support
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
            max-width: 800px;
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
            max-height: 400px;
            overflow-y: auto;
        }
        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .file-actions {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-top: 5px;
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
            flex-grow: 1;
            margin-right: 15px;
            word-break: break-all;
        }
        .file-thumbnail {
            width: 300px;
            height: 300px;
            object-fit: cover;
            margin-right: 20px;
            border-radius: 4px;
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
        <p>Mọi người upload thì giữ Ctrl + Chọn ảnh để có thể chọn được nhiều ảnh cùng 1 lúc, giữ Ctrl + lăn chuột để phóng to thumnnail giúp chọn ảnh chuẩn hơn, chọn Upload<p>
    </div>

    <div class="container">
        <h2>
            Uploaded Files
            <button onclick="window.location.href='/?page={{ current_page }}'" class="refresh-btn">Refresh</button>
        </h2>
        <div class="file-list">
            {% if files %}
                {% for file in files %}
                <div class="file-item">
                    <img src="/thumbnail/{{ file.name }}" class="file-thumbnail" alt="Thumbnail">
                    <div class="file-info">{{ file.name }} ({{ file.size }}) - {{ file.date }}</div>
                    <div class="file-actions">
                        <a href="/download/{{ file.name }}" class="btn">Download</a>
                        <a href="/delete/{{ file.name }}?page={{ current_page }}" class="btn btn-delete" onclick="return confirm('Bruh có chắc muốn xóa ảnh này?')">Delete</a>
                    </div>
                </div>
                {% endfor %}

                <div class="pagination">
                    {% if pages > 1 %}
                        {% if current_page > 1 %}
                            <button onclick="window.location.href='/?page={{ current_page - 1 }}'">←</button>
                        {% endif %}

                        {% for page in range(1, pages + 1) %}
                            <button onclick="window.location.href='/?page={{ page }}'" {% if page == current_page %}class="current-page"{% endif %}>{{ page }}</button>
                        {% endfor %}

                        {% if current_page < pages %}
                            <button onclick="window.location.href='/?page={{ current_page + 1 }}'">→</button>
                        {% endif %}
                    {% endif %}
                </div>
            {% else %}
                <p>No files in this folder.</p>
            {% endif %}
        </div>
    <p>Mn nên xóa bằng Delete trên trang này, không nên xóa trên Drive nên vì đôi lúc Drive không cập nhật sẽ bị lỗi, VD: Folder De_abc có 50 ảnh và bạn chỉ lấy 10 ảnh để Upscale bằng các xóa trên Drive nhưng vì Drive ko update kịp nên sẽ Upscale hết 50 ảnh * 2' = 100' rất tốn thời gian <p>
    </div>
    <p>hello<p>
</body>
</html>
'''

def create_flask_app(upload_folder):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

    # Helper function for Vietnamese folder names
    def sanitize_vietnamese_filename(filename):
        """Sanitize filename while preserving Vietnamese characters and slashes"""
        illegal_chars = ['\\', ':', '*', '?', '"', '<', '>', '|']
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename.strip()

    # Helper function to get human-readable file size
    def get_file_size(size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.1f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.1f} TB"

    # Helper function to get formatted date
    def get_formatted_date(timestamp):
        date = datetime.fromtimestamp(timestamp)
        vietnam_time = date + timedelta(hours=7)
        return vietnam_time.strftime("%Y-%m-%d %H:%M:%S")

    @app.route('/')
    def index():
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Number of files per page

        # Get the current folder path and remove the default path from the display
        folder_name_display = app.config['UPLOAD_FOLDER'].replace(upload_folder, '')

        # Get list of files in the current upload folder
        files = []
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            all_files = []
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(file_path):
                    # Check if it's an image file
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                        size = get_file_size(os.path.getsize(file_path))
                        mod_time = os.path.getmtime(file_path)
                        formatted_date = get_formatted_date(mod_time)
                        all_files.append({
                            'name': filename,
                            'size': size,
                            'date': formatted_date,
                            'timestamp': mod_time
                        })

            # Sort files by modification time (newest first)
            all_files.sort(key=lambda x: x['timestamp'], reverse=True)

            # Calculate pagination
            total_files = len(all_files)
            pages = (total_files + per_page - 1) // per_page  # Ceiling division

            # Adjust page if out of range
            if page < 1:
                page = 1
            elif page > pages and pages > 0:
                page = pages

            # Get files for current page
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            files = all_files[start_idx:end_idx]

        return render_template_string(
            HTML_TEMPLATE,
            folder_name=folder_name_display,
            files=files,
            success_message=request.args.get('message', ''),
            error_message=request.args.get('error', ''),
            current_page=page,
            pages=max(1, (len(files) + per_page - 1) // per_page) if files else 0
        )

    @app.route('/set_folder', methods=['POST'])
    def set_folder():
        folder_name = request.form.get('folder_name')
        if folder_name:
            # Handle Vietnamese characters properly
            folder_name = sanitize_vietnamese_filename(folder_name)

            # Use absolute path if provided, otherwise assume relative to default
            if not folder_name.startswith('/'):
                folder_name = os.path.join(upload_folder, folder_name)

            app.config['UPLOAD_FOLDER'] = folder_name

            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                message = f"Folder changed to: {app.config['UPLOAD_FOLDER']}"
                return redirect(url_for('index', message=message))
            except Exception as e:
                error = f"Error creating folder: {str(e)}"
                return redirect(url_for('index', error=error))
        else:
            return redirect(url_for('index', error="Please provide a valid folder name"))

    @app.route('/upload', methods=['POST'])
    def upload_file():
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
                    errors.append(f"Error uploading {file.filename}: {str(e)}")

        if errors:
            return redirect(url_for('index', error="\n".join(errors)))
        else:
            message = f"Successfully uploaded {upload_count} file(s)"
            return redirect(url_for('index', message=message))

    @app.route('/download/<filename>')
    def download_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

    @app.route('/thumbnail/<filename>')
    def thumbnail(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/delete/<filename>')
    def delete_file(filename):
        page = request.args.get('page', 1, type=int)
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                message = f"File {filename} deleted successfully"
            else:
                message = f"File {filename} not found"
            return redirect(url_for('index', message=message, page=page))
        except Exception as e:
            error = f"Error deleting file: {str(e)}"
            return redirect(url_for('index', error=error, page=page))

    return app

def run_flask_app(port=5000, upload_folder=None):
    if upload_folder is None:
        upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    app = create_flask_app(upload_folder)
    app.run(host='0.0.0.0', port=port)

def setup_serveo_tunnel(port=5000):
    """Set up a Serveo tunnel for the Flask app"""
    if shutil.which("ssh") is None:
        print("Installing openssh-client...")
        subprocess.run(["apt-get", "-qq", "update"])
        subprocess.run(["apt-get", "-qq", "install", "-y", "openssh-client"])
    
    process = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:localhost:{port}", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Read output to get the web link
    for line in iter(process.stdout.readline, ''):
        match = re.search(r'(https?://[^\s]+)', line)
        if match:
            public_url = match.group(1)
            print(f"\033[92m{'🔗 Photo Uploader Serveo URL:'}\033[0m {public_url}")
            return public_url, process
    
    return None, None 