from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World! My Flask App is working on Vercel!"

# This is very important for running it on your computer
if __name__ == '__main__':
    app.run(debug=True)
