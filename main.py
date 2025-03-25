# import libraries 
from flask import Flask, render_template, request, redirect, jsonify, url_for
import os 
from Werkzueg import secure_filename

# create an instance of Flask
app = Flask(__name__)

# landing page 
@app.route('/')
def index():
    return render_template('index.html')


# define allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
UPLOAD_FILE = 'uploads'

# check if file exists
os.makedirs(UPLOAD_FILE, exist_ok=True)

# helper function 

# post pdf or pptx file      
@app.route('/upload/', method=['POST'])
def upload_file():

    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == "":
            return jsonify({'error': 'No selected file'}), 400
        
        # check file extension 
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return jsonify({'error': 'Invalid file extension. Only PDF or PPTX'}), 400
                
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FILE, filename))
        # return redirect(url_for('index'))
        return redirect('/')

    return render_template('index.html')



# run server - python main.py   
if __name__ == '__main__':
    app.run(debug=True)
