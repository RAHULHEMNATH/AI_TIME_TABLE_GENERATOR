from http.server import BaseHTTPRequestHandler
import json
import traceback
import sys
import os

# Add the root project directory to the Python path so we can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Now try to import your Flask app from app.py
    from app import app as flask_app
    print("SUCCESS: Flask app imported!")
    
except Exception as e:
    # If import fails, we'll create a simple app that shows the error
    error_msg = traceback.format_exc()
    print(f"IMPORT FAILED: {error_msg}")
    
    from flask import Flask
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def show_import_error():
        return f"<h1>Import Error</h1><pre>{error_msg}</pre>", 500

# Create a simple handler for Vercel
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Capture the response from Flask
            with flask_app.test_request_context(path=self.path, method='GET'):
                response = flask_app.full_dispatch_request()
                
            self.send_response(response.status_code)
            
            for key, value in response.headers:
                self.send_header(key, value)
            self.end_headers()
            
            self.wfile.write(response.get_data())
            
        except Exception as e:
            error_msg = traceback.format_exc()
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Handler Error</h1><pre>{error_msg}</pre>".encode())

# This makes the function compatible with Vercel's serverless system
def vercel_handler(request):
    try:
        handler = Handler()
        handler.request = request
        handler.path = request['path']
        handler.command = request['httpMethod']
        handler.headers = request['headers']
        
        handler.do_GET()
        
        return {
            'statusCode': handler.status_code,
            'headers': dict(handler.headers),
            'body': handler.response_content.decode() if handler.response_content else ''
        }
    except Exception as e:
        error_msg = traceback.format_exc()
        return {
            'statusCode': 500,
            'body': f"<h1>Vercel Handler Error</h1><pre>{error_msg}</pre>"
        }

# The main function that Vercel will call
def main(request):
    return vercel_handler(request)