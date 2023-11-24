from flask import Flask, request, jsonify
from Mechanics.algorithms import ChatAlgorithm
from Mechanics.algorithms import ChatOutput

app = Flask(__name__)

@app.route('/find-prerequisite', methods=['POST'])
def find_prerequisite():
    data = request.json
    requested_course = data.get('request_course')

    
    

if __name__=='__main__':
    app.run(debug=True)