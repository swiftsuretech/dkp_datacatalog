from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route("/dashboard")
def hello_world():
    return "<p>Hello, World!</p>"