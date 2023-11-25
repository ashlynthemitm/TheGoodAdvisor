import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# from Mechanics.algorithms.ChatOutput import ChatOutput


# Set the path to the templates
app = Flask(__name__, 
            static_folder='../ChatUI/static', 
            template_folder='../ChatUI/templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/find_prerequisites', methods=['POST'])

# @app.route('/four_year_plan', methods=['POST'])
# def generate_four_year_plan():
#     data = request.json
#     # Initalize object
#     output = None
#     chat = ChatOutput(findFourYearPlan=True)
#     result = output.GenerateFourYearPlan(completed_courses=data.get("completed_courses"))
    
#     if output is not None:
#         return jsonify(result)
#     else:
#         return jsonify({"error": "No valid selection made"}), 400
  
if __name__=='__main__':
    app.run(debug=True)