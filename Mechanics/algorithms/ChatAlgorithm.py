'''
Full Algorithm for Chatbot Mechanics

Author: Ashlyn Campbell 
'''
from collections import namedtuple
from dotenv import load_dotenv
import mysql.connector
import os 
import re


class FourYearPlan:
    def __init__(self):
        self.four_year_plan = {'First Year': [[],[]], 'Second Year': [[],[]], 'Third Year': [[],[]], 'Fourth Year': [[],[]], 'Summer Semester':[[],[]]}
        self.current_year = 'First Year'
        self.current_semester = 0
        self.current_hours = 0
        
    def addCourse(self, course, credit_hours):
        # this adds courses to the four_year_plan
        if self.current_hours + credit_hours > 12:
            self.current_hours = 0
            if self.current_semester == 0:
                self.current_semester = 1
            else:
                self.current_semester = 0
                self.nextYear()
                    
        self.current_hours += credit_hours
        self.four_year_plan[self.current_year][self.current_semester].append(course)
                
    def nextYear(self):
        match(self.current_year):
            case 'First Year':
                self.current_year = 'Second Year'
            case 'Second Year':
                self.current_year = 'Third Year'
            case 'Third Year':
                self.current_year = 'Fourth Year'
            case _:
                # Fourth Year --> additional classes past four years
                print('Classes were not complete in time')
                print(self.current_year)
                print(self.current_semester)
                self.current_year = 'Summer Semester'
                
class ChatAlgorithm():
    def __init__(self, completed_courses):
        self.completed_courses = completed_courses
        self.priority_course_types = ['Core Curriculum', 'Major Requirements', ('Data Science Certificate Requirements', 'Data Science Certificate Choice'), ('Cybersecurity Certificate Requirements', 'Cybersecurity Certificate Choice')]
        self.swe_priority = set({'CSC 1302','MATH 2211','CSC 2510 or MATH 2420'})
        self.four_year_plan = FourYearPlan()
        self.inPlan = set() # This will be used to not readd any values
        self.course_credits = {}
        
        
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
        
    def FindPrerequisites(self, requested_courses, default=True):
        course_prerequisites = {}
        
        for course_code in requested_courses:
            find_prereqs_query = f"""
                SELECT
                    GROUP_CONCAT(p.prereq_name ORDER BY p.choice SEPARATOR ' or ') AS choice_prereqs,
                    p.prereq_course_id
                FROM
                    prerequisite p
                WHERE
                    p.course_code = '{course_code}'
                GROUP BY
                    p.prereq_course_id;
                """
        
            self.cursor.execute(find_prereqs_query)
            course_results = self.cursor.fetchall()
            course_prerequisites[course_code] = []
            for row in course_results: # the 0 column has the prerequisites
                course_prerequisites[course_code].append(row[0])
                
        return course_prerequisites
    
    def PopulateCoursework(self,i):
        courses_list = []
        course_count = 0
        if i > 1:
            find_courses_query = f"""
            SELECT c.course_code
            FROM Course c
            WHERE c.course_type IN {self.priority_course_types[i]} AND (c.credit_hours IS NOT NULL);
            """
        else:
            find_courses_query = f"""
                 SELECT c.course_code
                 FROM Course c
                 WHERE c.course_type = '{self.priority_course_types[i]}' AND (c.credit_hours IS NOT NULL);
            """
        self.cursor.execute(find_courses_query)
        course_results = self.cursor.fetchall()
        
        for row in course_results:
            courses_list.append(row[0])
            
        course_prerequisites = self.FindPrerequisites(courses_list, default=False) 
       
        for course in courses_list:
            match = re.fullmatch(r'\b[A-Z]{3,4} [0-9]{4}\b', course)
            if course in self.inPlan or (not match):
                continue 
            for prereq in course_prerequisites[course]:
                if ' or ' in prereq:
                    prereq_choices = prereq.split(' or ') 
                    if any(value in self.inPlan for value in prereq_choices):
                        continue
                    else:
                        prereq = prereq_choices[0]
                             
                match (prereq, course):
                    case 'MATH 2420':
                        self.inPlan.append('CSC 2510')
                    case 'CSC 2510':
                        self.inPlan.append('MATH 2420')
                if prereq in self.inPlan:
                    continue
                else: 
                    self.inPlan.add(prereq)
                    courses_list.append(prereq)
                    self.four_year_plan.addCourse(prereq, self.course_credits.get(prereq, 4))
            self.inPlan.add(course)
            courses_list.append(course)
            self.four_year_plan.addCourse(course, self.course_credits.get(course, 4))
            if i > 1:
                course_count += 1
            if course_count == 4:
                return 
            
        # by the end of this, the FourYearPlan should be populated
    
    def CreateFourYearPlan(self, isDataScience, isCYBER, isSWE):
        find_credits_query = """
            SELECT c.course_code, c.credit_hours
            FROM Course c;
        """
        self.cursor.execute(find_credits_query)
        credits_results = self.cursor.fetchall()
        for row in credits_results:
            course_code, credit_hours = row
            self.course_credits[course_code] = credit_hours
    
        self.PopulateCoursework(i=0)
        self.PopulateCoursework(i=1)
        if isDataScience:
            self.PopulateCoursework(i=2)
        elif isCYBER:
            self.PopulateCoursework(i=3)
        else:
            # no particular preference for certificate program
            self.certificate_courses = 'Pick any CSC 3000/4000 level courses, Add suggestions to this output'   
            for i in range(4):
                self.four_year_plan.addCourse(course='ANY CSC 3000/4000', credit_hours=4)

                
def main(completed_courses, find_prerequisites=False, create_four_year_plan=False, isDataScience=False, isCYBER=False, isSWE=False):
    with ChatAlgorithm(completed_courses) as chat:
        chat.cursor.execute('use thegoodadvisordb')
        
        # The User can either Find Prerequisites or Generate a Four Year Plan
        if find_prerequisites:
            print(chat.FindPrerequisites(find_prerequisites))
            
        # If Generate Four Year Plan is True
        for course in completed_courses:
            chat.inPlan.add(course)
        if create_four_year_plan:
            chat.CreateFourYearPlan(isDataScience, isCYBER, isSWE)
        
        print('inPlan: ', chat.inPlan)
        print(chat.four_year_plan.four_year_plan)
        chat.TheGoodAdvisor_db.commit()

if __name__ == '__main__':
    completed_courses = set()
    completed_courses.add('MATH 1111')
    main(completed_courses, find_prerequisites=False, create_four_year_plan=True, isDataScience=True, isCYBER=False, isSWE=True)
    
'''
Debugging Steps: 
1- Fix 2420 - 2510 error
2 - Add 2720 emphasis 
3 - Fix ChatOutput
(Clean up and be ready to explain/present)
'''