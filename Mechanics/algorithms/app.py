from flask import Flask, request, jsonify
import ChatOutput
import sys
sys.path.append('Mechanics/Chatbot/app.py')

app = Flask(__name__)
CORS(app)

@app.route('/process-request', methods=['POST'])
def process_request():
    data = request.json

    # Instantiate the ChatOutput class based on user's selection
    chat_output = ChatOutput(findPrerequisite=data.get('findPrerequisite', False),
                             findFourYearPlan=data.get('findFourYearPlan', False))
    
    output = None  # Initialize output

    # Process the request based on the user's selection
    if data.get('findPrerequisite'):
        output = chat_output.findPrerequisite(completed_courses=data.get('completed_courses'))
    elif data.get('findFourYearPlan'):
        output = chat_output.GenerateFourYearPlan(completed_courses=data.get('completed_courses'))
    # Add more conditions if needed

    if output is not None:
        return jsonify(output)
    else:
        return jsonify({"error": "No valid selection made"}), 400


if __name__=='__main__':
    app.run(debug=True)