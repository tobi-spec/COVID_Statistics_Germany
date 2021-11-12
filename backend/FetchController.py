from flask import Flask

import DIVIService
import RKIService

app = Flask(__name__)


@app.route('/')
def get_connection():
    return 'Hello, World! This server works fine!'


@app.route("/fetch/rki")
def fetch_rki():
    return RKIService.fetch()


@app.route("/fetch/divi")
def fetch_divi():
    return DIVIService.fetch()