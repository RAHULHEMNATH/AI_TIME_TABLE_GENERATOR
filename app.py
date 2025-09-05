from flask import Flask, render_template # Make sure to import render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Try to render your main homepage template
    # Replace 'index.html' with the name of your actual main template file
    return render_template('main.py')

if __name__ == '__main__':
    app.run(debug=True)
