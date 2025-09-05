from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "API folder test is working!"

# This makes it work on Vercel
def main(request):
    with app.test_request_context(path=request['path'], method=request['httpMethod']):
        response = app.full_dispatch_request()
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data().decode('utf-8')
    }
