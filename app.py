from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'drone-analysis-secret-key-2024'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads' if os.environ.get('VERCEL') else 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
        
        # Simple demo results (no actual AI analysis for Vercel compatibility)
        analysis_results = {
            'property_address': property_address,
            'analysis_date': datetime.now().isoformat(),
            'total_estimated_cost': 28500,
            'condition_score': 7.2,
            'categories': {
                'roof': {'cost': 12000, 'condition': 'Fair', 'priority': 'High'},
                'siding': {'cost': 8500, 'condition': 'Good', 'priority': 'Medium'},
                'landscaping': {'cost': 4000, 'condition': 'Needs Work', 'priority': 'Low'},
                'hardscaping': {'cost': 4000, 'condition': 'Fair', 'priority': 'Medium'}
            },
            'recommendations': [
                'Address roof issues before winter season',
                'Consider landscaping improvements for curb appeal',
                'Schedule gutter cleaning and maintenance'
            ]
        }
        
        return render_template('results.html', results=analysis_results)
    
    return render_template('upload.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    # Return demo results for API endpoint
    return jsonify({
        'status': 'success',
        'message': 'Demo analysis complete',
        'total_cost': 25000,
        'condition_score': 7.5
    })

if __name__ == '__main__':
    app.run(debug=True)