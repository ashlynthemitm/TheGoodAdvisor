from flask import Flask, render_template, request, jsonify
from ChatOutput import *
import os

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
def process_request(): # this method processes all data taken in
    data = request.json
    
    # Execute Functions based on input
    findPrereqs = data.get('find_prerequisites')
    createFourYearPlan = data.get('create_four_year_plan')
    if findPrereqs:
        return find_prerequisite_request(data)
    elif createFourYearPlan:
        return generate_four_year_plan_request(data)
    else:
         return jsonify({'message': 'Invalid request type'}), 400
  

@app.route('/generate-four-year-plan', methods=['POST'])
def generate_four_year_plan_request(data):
    # Extract needed data from the request
    completed_courses = data.get('completedCourses', [])
    is_data_science = data.get('isDataScience', False)
    is_cyber = data.get('isCYBER', False)
    is_swe = data.get('isSWE', False)

    # Instantiate the ChatOutput class
    chat_output = ChatOutput(findFourYearPlan=True)
    
    # Call the method to generate the four-year plan with correct parameters
    four_year_plan = chat_output.GenerateFourYearPlan(
        completed_courses=completed_courses,
        find_prerequisites=False,
        create_four_year_plan=True,
        isDataScience=is_data_science,
        isCYBER=is_cyber,
        isSWE=is_swe
    )
    print(four_year_plan)
    
    response = {
        'fourYearPlan':four_year_plan,
        'prerequisite': 'Empty'
    }
    return jsonify(response)
  
@app.route('/find-prerequisite', methods=['POST'])  
def find_prerequisite_request(data):
    completed_courses = data.get('completed_courses', [])
    find_prerequisites = data.get('find_prerequisites', True)
    is_data_science = data.get('isDataScience', False)
    is_cyber = data.get('isCYBER', False)
    is_swe = data.get('isSWE', False)
     
    # Instantiate the ChatOutput class
    chat_output = ChatOutput(findPrerequisite=True)
     
    prerequisite_output = chat_output.findPrerequisite(
        completed_courses=completed_courses,
        find_prerequisites=find_prerequisites,
        create_four_year_plan=False,  # Assuming this is not required for finding prerequisites
        isDataScience=is_data_science,
        isCYBER=is_cyber,
        isSWE=is_swe
    )
    
    print(prerequisite_output)
    response = {
        'fourYearPlan': 'Empty',
        'prerequisite': prerequisite_output
    }
    return jsonify(response)

if __name__=='__main__':
    app.run(debug=True)