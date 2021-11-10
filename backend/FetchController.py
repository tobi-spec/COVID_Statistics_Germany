from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_connection():
    return 'Hello, World! This server works fine!'

