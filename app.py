from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Simple test is working! If you see this, Flask works."

if __name__ == '__main__':
    app.run()
