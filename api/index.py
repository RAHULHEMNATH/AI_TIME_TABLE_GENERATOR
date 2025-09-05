from flask import Flask, render_template
import traceback
import os

app = Flask(__name__)

# Set the correct template folder path explicitly
app.template_folder = 'templates'

@app.route('/')
def home():
    try:
        # Check if templates folder and file exist
        template_path = os.path.join('templates', 'index.html')
        
        if not os.path.exists('templates'):
            return f"Templates folder not found! Current directory: {os.getcwd()}", 500
            
        if not os.path.exists(template_path):
            files = os.listdir('templates')
            return f"index.html not found in templates folder! Files found: {files}", 500
            
        # If everything exists, render the template
        return render_template('index.html')
        
    except Exception as e:
        error_msg = traceback.format_exc()
        return f"""
        <h1>Template Error Details</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Current directory:</strong> {os.getcwd()}</p>
        <p><strong>Templates exists:</strong> {os.path.exists('templates')}</p>
        <p><strong>Files in templates:</strong> {os.listdir('templates') if os.path.exists('templates') else 'NOT FOUND'}</p>
        <pre style='background: #f0f0f0; padding: 10px;'>{error_msg}</pre>
        """, 500

# Vercel handler function
def main(request):
    try:
        with app.test_request_context(path=request['path'], method=request['httpMethod']):
            response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data().decode('utf-8')
        }
    except Exception as e:
        error_msg = traceback.format_exc()
        return {
            'statusCode': 500,
            'body': f"<h1>Vercel Handler Error</h1><pre>{error_msg}</pre>"
        }
