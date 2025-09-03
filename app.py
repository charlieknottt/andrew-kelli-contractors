from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
import cv2
import numpy as np
from PIL import Image
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from property_analyzer import PropertyAnalyzer
from report_generator import ReportGenerator
import uuid

app = Flask(__name__)
app.secret_key = 'drone-analysis-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('reports', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No files selected')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        property_address = request.form.get('property_address', 'Unknown Property')
        
        if not files or files[0].filename == '':
            flash('No files selected')
            return redirect(request.url)
        
        session_id = str(uuid.uuid4())
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_folder, exist_ok=True)
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(session_folder, filename)
                file.save(file_path)
                uploaded_files.append(file_path)
        
        if uploaded_files:
            analyzer = PropertyAnalyzer()
            analysis_results = analyzer.analyze_property(uploaded_files)
            analysis_results['property_address'] = property_address
            analysis_results['session_id'] = session_id
            analysis_results['upload_date'] = datetime.now().isoformat()
            
            # Save analysis results
            results_file = os.path.join(session_folder, 'analysis_results.json')
            with open(results_file, 'w') as f:
                json.dump(analysis_results, f, indent=2)
            
            return render_template('results.html', results=analysis_results)
        else:
            flash('No valid image files uploaded')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/generate_report/<session_id>')
def generate_report(session_id):
    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    results_file = os.path.join(session_folder, 'analysis_results.json')
    
    if not os.path.exists(results_file):
        flash('Analysis results not found')
        return redirect(url_for('index'))
    
    with open(results_file, 'r') as f:
        analysis_results = json.load(f)
    
    report_generator = ReportGenerator()
    report_path = report_generator.generate_report(analysis_results, session_id)
    
    return send_file(report_path, as_attachment=True, download_name=f'property_analysis_{session_id}.pdf')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    session_id = str(uuid.uuid4())
    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_folder, exist_ok=True)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(session_folder, filename)
    file.save(file_path)
    
    analyzer = PropertyAnalyzer()
    analysis_results = analyzer.analyze_property([file_path])
    
    return jsonify(analysis_results)

# For Vercel deployment
import tempfile

# Override upload folder for serverless environment
if os.environ.get('VERCEL'):
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    os.makedirs('/tmp/uploads', exist_ok=True)
    os.makedirs('/tmp/reports', exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)