from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # or whatever your main template is

# Add your other routes here

# This is important for Vercel
if __name__ == '__main__':
    app.run()
else:
    # This makes the app compatible with Vercel's serverless functions
    import sys
    from io import StringIO
    from flask import request
    
    # Create a simple WSGI adapter for Vercel
    def vercel_handler(request):
        from werkzeug.wrappers import Response
        
        # Capture stdout/stderr
        old_stdout, old_stderr = sys.stdout, sys.stderr
        captured_output, captured_errors = StringIO(), StringIO()
        
        try:
            sys.stdout, sys.stderr = captured_output, captured_errors
            
            # Process the request through Flask
            with app.request_context(request):
                response = app.full_dispatch_request()
                
            # Return the response in Vercel's expected format
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data().decode('utf-8')
            }
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr

# This allows the app to work both locally and on Vercel
app.vercel_handler = vercel_handler


from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World! My Flask App is working on Vercel!"

# This is very important for running it on your computer
if __name__ == '__main__':
    app.run(debug=True)
