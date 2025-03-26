from flask import Blueprint, render_template, request, flash, redirect, url_for
from extensions import db
from .models import FileUploaded, ParsedData
from parser import extract_pdf_data, extract_pptx_data
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
import os
import uuid
from datetime import datetime

web_bp = Blueprint('web', __name__)


# @web_bp.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         if 'file' not in request.files:
#             flash('No file part', 'error')
#             return redirect(url_for('web.index'))

#         file = request.files['file']

#         if file.filename == "":
#             flash('No selected file', 'error')
#             return redirect(url_for('web.index'))

#         # Check file size
#         if file.content_length > MAX_FILE_SIZE:
#             flash('File too large. Max file size is 12MB', 'error')
#             return redirect(url_for('web.index'))
        
#         # Check file content
#         if file.content_length == 0:
#             flash('Empty file', 'error')
#             return redirect(url_for('web.index'))

#         # Check file extension
#         if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
#             flash('Unsupported file extension. Only PDF or PPTX are allowed', 'error')
#             return redirect(url_for('web.index'))

#         # Generate a secure unique filename 
#         file_ext = file.filename.rsplit('.', 1)[1].lower()
#         unique_filename = f"{datetime.now().strftime('%Y%m%d_%I-%M%p')}_{uuid.uuid4().hex}.{file_ext}"
#         file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

#         try:
#             file.save(file_path)
#             os.chmod(file_path, 0o640)

#             # Save uploaded file 
#             uploaded_file = FileUploaded(filename=unique_filename, file_type=file_ext)
#             db.session.add(uploaded_file)
#             db.session.commit()

#             # Extract parsed data and save 
#             parsed_content, error = None, None
#             if file_ext == "pdf":
#                 parsed_content, error = extract_pdf_data(file_path)
#             elif file_ext == "pptx":
#                 parsed_content, error = extract_pptx_data(file_path)
                
#             if error:
#                 flash(f"Error parsing file: {error}", 'error')
#                 return redirect(url_for('web.index'))

#             parsed_data = ParsedData(file_id=uploaded_file.id, content=parsed_content)
#             db.session.add(parsed_data)
#             db.session.commit()

#             flash('File uploaded and processed successfully!', 'success')
#             return render_template("results.html", 
#                                 filename=unique_filename,
#                                 content=parsed_content,
#                                 file_type=file_ext.capitalize())
            
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error processing file: {str(e)}', 'error')
#             return redirect(url_for('web.index'))
    
#     # For GET requests or if there were no files uploaded
#     uploaded_files = FileUploaded.query.order_by(FileUploaded.upload_date.desc()).limit(5).all()
#     return render_template("index.html", recent_files=uploaded_files)

@web_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('web.index'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('web.index'))

        # Check file extension first (quick check)
        if not ('.' in file.filename and 
               file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            flash('Unsupported file extension. Only PDF or PPTX are allowed', 'error')
            return redirect(url_for('web.index'))

        # Generate secure filename
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%I-%M%p')}_{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        try:
            # Save file first, then check size
            file.save(file_path)
            actual_size = os.path.getsize(file_path)
            
            if actual_size == 0:
                os.remove(file_path)  # Clean up empty file
                flash('Uploaded file is empty', 'error')
                return redirect(url_for('web.index'))
                
            if actual_size > MAX_FILE_SIZE:
                os.remove(file_path)  # Clean up oversized file
                flash('File too large. Max file size is 12MB', 'error')
                return redirect(url_for('web.index'))

            os.chmod(file_path, 0o640)

            # Rest of your processing logic...
            uploaded_file = FileUploaded(filename=unique_filename, file_type=file_ext)
            db.session.add(uploaded_file)
            db.session.commit()

            parsed_content, error = None, None
            if file_ext == "pdf":
                parsed_content, error = extract_pdf_data(file_path)
            elif file_ext == "pptx":
                parsed_content, error = extract_pptx_data(file_path)
                
            if error:
                flash(f"Error parsing file: {error}", 'error')
                return redirect(url_for('web.index'))

            parsed_data = ParsedData(file_id=uploaded_file.id, content=parsed_content)
            db.session.add(parsed_data)
            db.session.commit()

            flash('File uploaded and processed successfully!', 'success')
            return render_template("results.html", 
                                filename=unique_filename,
                                content=parsed_content,
                                file_type=file_ext.capitalize())
            
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.rollback()
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('web.index'))
    
    # GET request handling
    uploaded_files = FileUploaded.query.order_by(FileUploaded.upload_date.desc()).limit(5).all()
    return render_template("index.html", recent_files=uploaded_files)


@web_bp.route('/files')
def list_files():
    files = FileUploaded.query.order_by(FileUploaded.upload_date.desc()).all()
    return render_template("files.html", files=files)


@web_bp.route('/files/<int:file_id>')
def view_file(file_id):
    file_data = ParsedData.query.filter_by(file_id=file_id).first()
    if not file_data:
        flash('File not found', 'error')
        return redirect(url_for('web.list_files'))
    
    original_file = FileUploaded.query.get(file_id)
    return render_template("file_detail.html", 
                         content=file_data.content,
                         filename=original_file.filename,
                         upload_date=original_file.upload_date)