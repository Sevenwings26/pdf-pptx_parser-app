# Import libraries  
from flask import Flask, render_template, request, redirect, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid   # to generate unique filenames and save
from parser import extract_pdf_data, extract_pptx_data
from flask_sqlalchemy import SQLAlchemy


# Create an instance of Flask
app = Flask(__name__)

# Define allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 12 * 1024 * 1024  # 12MB max file size
basedir = os.path.abspath(os.path.dirname(__file__))


# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure Flask app to use the upload folder and max file size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_FILE_LENGTH'] = MAX_FILE_SIZE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'parser.db') 

db = SQLAlchemy(app)


# models 
class FileUploaded(db.Model):
    """Üploaded File"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class ParsedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file_uploaded.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file = db.relationship("FileUploaded", backref=db.backref('parsed_data', lazy=True))


# initialize db   
with app.app_context():
    db.create_all()
    print("Database Created")



# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# POST route to upload PDF or PPTX files      
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == "":
        return jsonify({'error': 'No selected file'}), 400

    # Check file size
    if file.content_length > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large. Max file size is 12MB'}), 400
    
    # Check file content
    if file.content_length == 0:
        return jsonify({'error': 'Empty file'}), 400

    # Check file extension
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Unsupported file extension. Only PDF or PPTX are allowed'}), 400

    # Generate a secure unique filename 
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{datetime.now().strftime('%Y%m%d_%I-%M%p')}_{uuid.uuid4().hex}.{file_ext}"
    print(unique_filename)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        file.save(file_path)
        os.chmod(file_path, 0o640)

        # save uploaded file 
        uploaded_file = FileUploaded(filename=unique_filename, file_type=file_ext)
        db.session.add(uploaded_file)
        db.session.commit()

        # extract parsed data and save 
        parsed_content, error = None, None
        if file_ext == "pdf":
            parsed_content, error = extract_pdf_data(file_path)
        elif file_ext == "pptx":
            parsed_content, error = extract_pptx_data(file_path)
        if error:
            return jsonify({"error":error}), 500

        parsed_data = ParsedData(file_id=uploaded_file.id, content=parsed_content)
        db.session.add(parsed_data)
        db.session.commit()


        return jsonify({
            "message": "File uploaded successfully", 
            "filename": unique_filename,
            "file_path":file_path
            }), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error':str(e)}), 500
    

# GET all upload files
@app.route('/uploaded_files', methods=['GET'])
def get_uploaded_files():
    files = FileUploaded.query.all()
    try:
        results = [
            {
                "id": file.id,
                "filename": file.filename,
                "file_type": file.file_type,
                "upload_date": file.upload_date
            } 
            for file in files
        ]
        return jsonify({"files":results})
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# GET all parsed files
@app.route('/parsed_files', methods=['GET'])
def get_parsed_files():
    files = ParsedData.query.all()
    try:
        results = [
            {
                "parsed_id": file.id,
                "file_id": file.file_id,
                "content": file.content,
            } 
            for file in files
        ]
        return jsonify({"files":results})
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# GET single file
@app.route('/parsed_files/<int:file_id>', methods=['GET'])
def get_single_file(file_id):
    file = ParsedData.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404
    return jsonify({
        "parsed_id": file.id,
        "content": file.content,
    }), 200


# Run the server - Run `python main.py`  
if __name__ == '__main__':
    app.run(debug=True)
