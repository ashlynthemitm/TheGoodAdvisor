from flask import Flask, render_template, request, jsonify
import os
import ChatOutput

template_dir = os.path.abspath('./ChatUI/templates')
static_dir = os.path.abspath('./ChatUI/static')
# Set the path to the templates
app = Flask(__name__, 
            static_folder=static_dir, 
            template_folder=template_dir)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-request', methods=['POST'])
def process_request():
    data = request.json
    student_type = data.get('studentType')
    
    if student_type == 'four-year-plan':
        return process_four_year_plan_request(data)
    else:
         return jsonify({'message': 'Invalid request type'}), 400

@app.route('/process-four-year-plan', methods=['POST'])
def process_four_year_plan_request(data):
    completed_courses = data.get('completedCourses', [])

if __name__=='__main__':
    app.run(debug=True)