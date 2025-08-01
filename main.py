from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/abstract')
def abstract():
    return render_template('abstract.html')

@app.route('/upload')
def upload():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/analysis')
def analysis():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('analysis.html')

@app.route('/result')
def result():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    return render_template('result.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'kowsi' and password == '2002':
        session['logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read and process the file
        try:
            df = pd.read_csv(filepath)
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'data': df.to_dict('records')
            })
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'})
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features from the request
        features = [
            float(data['sub1']),
            float(data['sub2']),
            float(data['sub3']),
            float(data['sub4']),
            float(data['sub5']),
            float(data['attendance']),
            float(data['studyHours']),
            float(data['activities'])
        ]
        
        # Placeholder for ML model prediction
        # You would replace this with your actual model prediction
        prediction = {
            'success': True,
            'prediction': 1 if np.mean(features[:5]) > 60 and features[5] > 75 else 0,
            'confidence': 0.85,
            'recommendations': []
        }
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
