import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


# Set the path to the templates
app = Flask(__name__, static_folder='ChatUI/static', template_folder='ChatUI/templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)