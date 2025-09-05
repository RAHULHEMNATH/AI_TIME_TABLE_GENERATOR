from flask import Flask
import traceback
import sys
import os

# Add the main project folder to Python's search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to import your REAL Flask app from app.py
try:
    from app import app  # This imports your actual Flask app
    print("SUCCESS: Your main app was imported!")
    
except Exception as e:
    # If importing fails, create a simple app that shows the error
    app = Flask(__name__)
    error_msg = traceback.format_exc()
    
    @app.route('/')
    def show_error():
        return f"""
        <h1>Error Importing Your App</h1>
        <p>There is a problem in your <code>app.py</code> file:</p>
        <pre style='background: #f0f0f0; padding: 10px;'>{error_msg}</pre>
        """, 500

# This makes it work on Vercel
def main(request):
    with app.test_request_context(path=request['path'], method=request['httpMethod']):
        response = app.full_dispatch_request()
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data().decode('utf-8')
    }
