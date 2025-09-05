from flask import Flask, render_template
import traceback
import sys

app = Flask(__name__)

# Try to import and setup your actual application
try:
    # --- This is where YOUR code starts ---
    # Add your original configuration here (one step at a time)
    # For example, if you use a database, uncomment these lines:
    # from flask_sqlalchemy import SQLAlchemy
    # db = SQLAlchemy(app)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    # Import your routes (if you have a routes.py file)
    # from routes import main_bp
    # app.register_blueprint(main_bp)

    # --- This is where YOUR code ends ---

    print("SUCCESS: App was imported and configured without any errors!")

except Exception as e:
    # This catches any error during setup
    print("ERROR during app setup:")
    print(traceback.format_exc())
    @app.route('/')
    def setup_error():
        error_msg = traceback.format_exc()
        return f"<h1>Setup Error</h1><pre>{error_msg}</pre>", 500

# Now try to handle a request
@app.route('/')
def home():
    try:
        # Try to render your template
        return render_template('index.html')
    except Exception as e:
        # If there's an error rendering the template, show it
        error_msg = traceback.format_exc()
        return f"<h1>Route Error</h1><pre>{error_msg}</pre>", 500

@app.errorhandler(500)
def internal_error(error):
    # This catches any other unhandled errors
    error_msg = traceback.format_exc()
    return f"<h1>Unhandled Error</h1><pre>{error_msg}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)
