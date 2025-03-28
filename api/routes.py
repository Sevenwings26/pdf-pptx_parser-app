from . import api_ns  
from flask_restx import fields, Resource
from flask import request, jsonify
from extensions import db
from web.models import FileUploaded, ParsedData
from parser import extract_pdf_data, extract_pptx_data
import os
import uuid
from datetime import datetime
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

# Use api_ns (your namespace) instead of api
upload_model = api_ns.model('UploadedFile', {
    'id': fields.Integer(description="File ID"),
    'filename': fields.String(required=True, description='Uploaded file name'),
    'file_type': fields.String(description="File type (PDF/PPTX)"),
    'upload_date': fields.DateTime(description="Upload timestamp")
})

parsed_model = api_ns.model('ParsedFile', {
    'parsed_id': fields.Integer(description="Parsed File ID"),
    'file_id': fields.Integer(description="ID of the uploaded file"),
    'content': fields.String(description="Extracted text content")
})

from tasks.celery import process_file

@api_ns.route('/upload/')
class UploadFile(Resource):
    @api_ns.doc(description="Upload PDF or PPTX files")
    @api_ns.response(200, 'Success', upload_model)
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(500, 'Internal Server Error')
    def post(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == "":
            return jsonify({'error': 'No selected file'}), 400
        
        if file.content_length > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Max file size is 12MB'}), 400
        
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return jsonify({'error': 'Unsupported file extension. Only PDF or PPTX are allowed'}), 400

        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%I-%M%p')}_{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        try:
            file.save(file_path)
            os.chmod(file_path, 0o640)
            uploaded_file = FileUploaded(filename=unique_filename, file_type=file_ext)
            db.session.add(uploaded_file)
            db.session.commit()

            parsed_content, error = None, None
            if file_ext == "pdf":
                parsed_content, error = extract_pdf_data(file_path)
            elif file_ext == "pptx":
                parsed_content, error = extract_pptx_data(file_path)
            
            if error:
                return jsonify({"error": error}), 500

            parsed_data = ParsedData(file_id=uploaded_file.id, content=parsed_content)
            db.session.add(parsed_data)
            db.session.commit()
            
            task = process_file.delay(file_path)
            return jsonify({
                "id": uploaded_file.id,
                "filename": unique_filename,
                "file_type": file_ext,
                "upload_date": uploaded_file.upload_date.isoformat(),
                "task_id": task.id,
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# GET all upload files
@api_ns.route('/uploaded_files')
class UploadedFiles(Resource):
    @api_ns.doc(description="Get all uploaded files")
    @api_ns.marshal_list_with(upload_model)
    def get(self):
        files = FileUploaded.query.all()
        return files

# GET all parsed files
@api_ns.route('/parsed_files')
class ParsedFiles(Resource):
    @api_ns.doc(description="Get all parsed files")
    @api_ns.marshal_list_with(parsed_model)
    def get(self):
        files = ParsedData.query.all()
        return files

# GET single file
@api_ns.route('/parsed_files/<int:file_id>')
class SingleFile(Resource):
    @api_ns.doc(description="Get single parsed file")
    @api_ns.marshal_with(parsed_model)
    def get(self, file_id):
        file = ParsedData.query.get_or_404(file_id)
        return file