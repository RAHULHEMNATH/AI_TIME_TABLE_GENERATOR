from flask import Flask, render_template
import traceback
import os

app = Flask(__name__)

# Try to render your main template
@app.route('/')
def home():
    try:
        # Try to render your main page template
        return render_template('index.html')
    except Exception as e:
        # Show detailed error if template fails
        error_msg = traceback.format_exc()
        return f"""
        <h1>Template Error</h1>
        <p>Could not render template:</p>
        <pre style='background: #f0f0f0; padding: 10px;'>{error_msg}</pre>
        <p>Current working directory: {os.getcwd()}</p>
        <p>Files in directory: {os.listdir('.')}</p>
        <p>Templates folder exists: {os.path.exists('templates')}</p>
        <p>Files in templates folder: {os.listdir('templates') if os.path.exists('templates') else 'NOT FOUND'}</p>
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
