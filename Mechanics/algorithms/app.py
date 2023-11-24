from flask import Flask, request, jsonify
import ChatOutput
import sys
sys.path.append('Mechanics/Chatbot/app.py')

app = Flask(__name__)

@app.route('/procces-request', methods=['Post'])
def process_request():
    data = request.json

    # Instantiate the ChatOutput class based on user's selection
    chat_output = ChatOutput(findPrerequisite=data.get('findPrerequisite', False),
                             findFourYearPlan=data.get('findFourYearPlan', False))

    # Process the request based on the user's selection
    if data.get('findPrerequisite'):
        output = chat_output.findPrerequisite(completed_courses=data.get('completed_courses'))
    elif data.get('findFourYearPlan'):
        output = chat_output.GenerateFourYearPlan(completed_courses=data.get('completed_courses'))
    # Add more conditions if needed

    return jsonify(output)

if __name__=='__main__':
    app.run(debug=True)