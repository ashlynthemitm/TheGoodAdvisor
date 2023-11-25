import os
import sys
from flask import Flask, render_template, request, jsonify
from Mechanics.algorithms.ChatOutput import ChatOutput

from flask_cors import CORS


# Set the path to the templates
app = Flask(__name__, 
            static_folder='../ChatUI/static', 
            template_folder='../ChatUI/templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    print(sys.path)
    app.run(debug=True)