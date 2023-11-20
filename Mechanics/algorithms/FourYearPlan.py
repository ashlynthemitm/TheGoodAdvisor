'''
Four Year Plan Algorithm based on previous input of previous coursework or 0 credits.
Author: Ashlyn Campbell 
'''
import mysql.connector
from dotenv import load_dotenv
import os 
import FindPreReq

class DeterminePlan():
    
    def __init__(self, completed_courses):
        self.priority_stack = ['Core Curriculum', 'Major Requirements', 'Data Science Certificate Choice', 'Cybersecurity Certificate Choice']
        self.completed_courses = completed_courses
        self.core_courses = []
        self.major_courses = []
        self.certificate = []
        self.four_year_plan = {'First Year': [[],[]], 'Second Year': [[],[]], 'Third Year': [[],[]], 'Fourth Year': [[],[]]}
        self.total_core = 18 # creds required
        
    def __enter__(self):
        try:
            load_dotenv()
            host_db = os.getenv('DB_HOST')
            username_db = os.getenv('DB_USERNAME')
            password_db = os.getenv('DB_PASSWORD')
            self.TheGoodAdvisor_db = mysql.connector.connect(
                host=host_db,
                user=username_db,
                password=password_db
            )
            self.cursor = self.TheGoodAdvisor_db.cursor()
            return self
        except mysql.connector.Error as error:
            print(f'Error: {error}')

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f'Exception Type: {exc_type}')
            print(f'Exception Value: {exc_value}')
        self.cursor.close()
        self.TheGoodAdvisor_db.close()

    def priorityFunc(self, i):
        find_priority_query = f"""
            SELECT c.course_code AS Core_Course, c.credit_hours AS Core_Course_Credit,
            p.prereq_name AS Prerequisite, pc.credit_hours AS Prereq_Credit
            FROM Course c
            JOIN Prerequisite p ON c.course_code = p.course_code
            LEFT JOIN Course pc ON p.prereq_name = pc.course_code
            WHERE c.course_type = '{self.priority_stack[i]}'
            AND c.course_code NOT IN '{self.completed_courses}'; 
        """
        
        return find_priority_query
    
    def FindCourseType(self, i): # begin with core classes
        
        # The required class for Certificate programs include requirements
        find_major_type_query = None
        if i > 1 or None:
            if i == 2:
                # Data Science Certificate Requirements
                find_major_type_query = f"""
                SELECT c.course_code
                FROM Course c
                WHERE c.course_type = 'Data Science Certificate Requirements';
            """
            else:
                find_major_type_query = f"""
                    SELECT c.course_code
                    FROM Course c
                    WHERE c.course_type = 'Cybersecurity Certificate Requirements';
                """    
        if i:
            find_course_type_query = f"""
                SELECT c.course_code
                FROM Course c
                WHERE c.course_type = '{self.priority_stack[i]}';
            """
        
        return find_course_type_query, find_major_type_query
    
    def getPrerequsite(self, requested_course): # get one prerequisite
        find_prereq_query = f"""
            SELECT p.prereq_name, p.choice, p.prereq_course_id
            FROM prerequisite p 
            LEFT JOIN course c ON c.course_id = p.course_id
            WHERE p.course_code = '{requested_course}'
            GROUP BY p.prereq_name, p.choice, p.prereq_course_id;
            """
        
        return find_prereq_query
    
    def getCreditHours(self, requested_course):
        find_credits_query = f"""
            SELECT c.credit_hours
            FROM Course c
            WHERE c.course_code = '{requested_course}';
        """
        
        return find_credits_query
       
def main(completed_courses, isDataScience, isCyberSecurity, isSWE):
    with DeterminePlan(completed_courses) as dp:
        dp.cursor.execute('use thegoodadvisordb')
        
        # Core Requirements 
        find_core_list_query = dp.FindCourseType(0)[0] 
        dp.cursor.execute(find_core_list_query)
        core_course_list = dp.cursor.fetchall() 
        
        # Some Courses are choices (maintain this dictionary to store each)
        choice_values = {}
        
        for core_course in core_course_list: # add the core courses to the list
            # check if the course has been taken
            if core_course in completed_courses:
                continue
            else:
                # check if the prerequsites have been taken
                find_prerequisite_query = dp.getPrerequsite(core_course)
                dp.cursor.execute(find_prerequisite_query)
                prerequisite_list = dp.cursor.fetchall() 
                # This loop will add all Prerequisites 
                for prerequisite_info in prerequisite_list:
                    prereq_code, isChoice, prereq_course_id = prerequisite_info
                    if isChoice:
                        # if it's a prerequisite that's a choice it's stored as the id in dp.core_classes
                        if prereq_course_id in choice_values:
                            choice_values[prereq_course_id].append(prereq_code)
                            dp.completed_courses.add(prereq_code) 
                        else:
                            choice_values[prereq_course_id] = [prereq_code]
                            dp.completed_courses.add(prereq_code)
                        
                        if prereq_code not in completed_courses:
                            dp.core_courses.append(prereq_course_id)
                        
                    else: # the prerequisite is not a choice and must be taken
                        dp.core_courses.append(prereq_code)
                        
            # Add the core_course after all prerequisites have been entered to maintain the order
            dp.core_courses.append(core_course)
            dp.completed_courses.add(core_course)
        
        # typically freshmen have only taken pre-core and core requirements, but I may still use the complete_courses set
        
        # Major Requirements
        find_major_list_query = dp.FindCourseType(1)[0]
        dp.cursor.execute(find_major_list_query)
        major_course_list = dp.cursor.fetchall() 
        
        for major_course in major_course_list:
            # check if the course has been taken (even in core requirements)
            if major_course in completed_courses:
                continue
            else:
                # check if the prerequisites have been taken
                find_prerequisite_query = dp.getPrerequsite(major_course)
                dp.cursor.execute(find_prerequisite_query)
                prerequisite_list = dp.cursor.fetchall() 
                
                for prerequisite_info in prerequisite_list:
                    prereq_code, isChoice, prereq_course_id = prerequisite_info
                    if isChoice:
                        # if it's a prerequisite that's a choice it's stored as the id in dp.core_classes
                        if prereq_course_id in choice_values:
                            choice_values[prereq_course_id].append(prereq_code)
                            dp.completed_courses.add(prereq_code) 
                        else:
                            choice_values[prereq_course_id] = [prereq_code]
                            dp.completed_courses.add(prereq_code)
                        
                        if prereq_code not in completed_courses:
                            dp.core_courses.append(prereq_course_id)
                        
                    else: # the prerequisite is not a choice and must be taken
                        dp.core_courses.append(prereq_code)
                        
            # Add the major_course after all prerequisites have been entered to maintain the order
            dp.major_courses.append(major_course)
            dp.completed_courses.add(major_course)
            
            
        # Additional 3000 - 4000 level courses
        if isDataScience or isCyberSecurity:
            if isDataScience:
                find_additional_list_query, required_course = dp.FindCourseType(2)
            else:
                find_additional_list_query, required_course = dp.FindCourseType(3)
            dp.cursor.execute(find_additional_list_query)
            additional_course_list = dp.cursor.fetchall()
        
        if not isDataScience and not isCyberSecurity:
            dp.certificate = False
            # The student has no preference, offer 3000-4000 level courses 
            # Suggest they explore the catalog and choose 4 classes to take
        else:
            dp.certificate.append(required_course)
            for additional_course in additional_course_list:
                dp.certificate.append(additional_course) # Prerequisites will be factored in later


        '''
        Next Steps: 
            - After all the course_work lists are populated add to four_year plan based on credit_hours 
            - query and add until <= 3 classes in CS assigned to each semester
            
        1. Create a query to look into each list in parallel, (i,j,k) and find the best course to take 
        2. Once the four-year plan is created there needs to be generic output to display the plan
        3. After this is set, the SWE plan can be added to this module and primarily preference 2720 and 
        other SWE related courses pulled from the website
        
        '''
        
        # Set up four_year_plan dictionary by querying through each list of courses for priority
        # q = ['First Year', 'Second Year', 'Third Year', 'Fourth Year']
        # credit_hours = 18 # subtract by credit_hours to fill up
        # currentSemester = 0 # switch between 0 & 1 to represent the semesters in the year
        # key = q.pop(0)
        
        # Test - print the courses lists
        
        
                    
        
        
        # prioritize 2720 and other notable SWE courses in this four_year_plan query
        
        
        dp.TheGoodAdvisor_db.commit()
        print(dp.core_courses)
        print(dp.major_courses)
        print(dp.certificate)
        print('Four Year Plan Complete')
        return

if __name__ == '__main__':
    print(main(completed_courses=('MATH 1111', 'MATH 1113'), isDataScience=False, isCyberSecurity=False, isSWE=False)) # printing for now, the dictionary needs to be returned to the calling class