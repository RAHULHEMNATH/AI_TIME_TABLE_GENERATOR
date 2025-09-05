from flask import Flask, render_template
import traceback

# Create Flask app
app = Flask(__name__)

# Try to import your templates and routes
try:
    @app.route('/')
    def home():
        return render_template('index.html')
    
    print("SUCCESS: Basic routes added!")
    
except Exception as e:
    error_msg = traceback.format_exc()
    print(f"ERROR: {error_msg}")
    
    @app.route('/')
    def show_error():
        return f"""
        <h1>Template Error</h1>
        <p>Could not load templates:</p>
        <pre style='background: #f0f0f0; padding: 10px;'>{error_msg}</pre>
        """, 500

# Vercel handler function
def main(request):
    with app.test_request_context(path=request['path'], method=request['httpMethod']):
        response = app.full_dispatch_request()
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data().decode('utf-8')
    }
