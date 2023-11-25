'''
Full Algorithm for Chatbot Mechanics includes a FourYearPlan Class to handle coursework separation and a full Algorithm Class to compute the different Chatbot capabilities such as Finding Prerequisites and Generating an efficient FourYearPlan

Author: Ashlyn Campbell 
'''
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
        self.current_courses = set()
        self.taken_courses = set()
        
    def addCourse(self, course, credit_hours):
        if self.current_hours + credit_hours > 12:
            self.nextSemester()
        self.current_hours += credit_hours
        self.four_year_plan[self.current_year][self.current_semester].append(course)   
            
    def nextSemester(self):
        self.current_hours = 0
        if (self.current_semester + 1 )> 1:
            self.current_semester = 0
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
                    print(self.current_year) # Error Handling
                    print(self.current_semester)
                    self.current_year = 'Summer Semester'
        else:
            self.current_semester = 1
        
        self.taken_courses.update(self.current_courses) # When the semester changes classes are views as taken

    def removeEquivalent(self, course, courses_list):
        match (course):
            case 'MATH 2420':
                self.current_courses.add('CSC 2510')
                if 'CSC 2510' in courses_list:
                    courses_list.remove('CSC 2510')
                    courses_list.remove('MATH 2420')
            case 'CSC 2510':
                self.current_courses.add('MATH 2420')
                if 'MATH 2420' in courses_list:
                    courses_list.remove('MATH 2420')
                    courses_list.remove('CSC 2510')
            case _:
                if course in courses_list:
                    courses_list.remove(course)
        return courses_list
                
class ChatAlgorithm():
    def __init__(self, completed_courses):
        self.completed_courses = completed_courses
        self.priority_course_types = ['Core Curriculum', 'Major Requirements', ('Data Science Certificate Requirements', 'Data Science Certificate Choice'), ('Cybersecurity Certificate Requirements', 'Cybersecurity Certificate Choice')]
        self.swe_priority = set({'CSC 1302','MATH 2211','CSC 2510 or MATH 2420'})
        self.four_year_plan = FourYearPlan()
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
            if row[0] != 'MATH 2215': # this course isnt required for this initial demo
                courses_list.append(row[0])
            
        course_prerequisites = self.FindPrerequisites(courses_list, default=False) 
        # add another layer to tailor towards the list looking at the entirety
        while courses_list: # remove courses from list 
            for index, course in enumerate(courses_list):
                match = re.fullmatch(r'\b[A-Z]{3,4} [0-9]{4}\b', course)
                if not match:
                    courses_list = self.four_year_plan.removeEquivalent(course, courses_list)
                if course in ((self.four_year_plan.taken_courses) or (self.four_year_plan.current_courses)):
                    continue
                else: 
                    missingPrerequisite = False
                    for prereq in course_prerequisites[course]:
                        if ' or ' in prereq:
                            prereq_choices = prereq.split(' or ') 
                            if any(value in (self.four_year_plan.taken_courses) for value in prereq_choices):
                                continue
                            elif not any(value in (self.four_year_plan.taken_courses and self.four_year_plan.current_courses) for value in prereq_choices): 
                                self.four_year_plan.addCourse(prereq_choices[0], self.course_credits.get(prereq_choices[0], 4))
                                self.four_year_plan.current_courses.add(prereq_choices[0])
                                missingPrerequisite = True
                            elif prereq_choices[0] in self.four_year_plan.current_courses:
                                missingPrerequisite = True
                            
                            courses_list = self.four_year_plan.removeEquivalent(prereq_choices[0], courses_list)
                            
                        else: # no or statement, check if in taken
                            if prereq in self.four_year_plan.taken_courses:
                                continue
                            elif prereq not in (self.four_year_plan.taken_courses or self.four_year_plan.current_courses):
                                self.four_year_plan.addCourse(prereq, self.course_credits.get(prereq, 4))
                                self.four_year_plan.current_courses.add(prereq)
                                missingPrerequisite = True
                            elif prereq in self.four_year_plan.current_courses:
                                missingPrerequisite = True
                                
                            courses_list = self.four_year_plan.removeEquivalent(prereq, courses_list)
                                
                    if not missingPrerequisite:
                        # All prerequisites are in taken_courses set so course can be added
                        courses_list = self.four_year_plan.removeEquivalent(course, courses_list)
                        self.four_year_plan.addCourse(course, self.course_credits.get(course, 4))
                        self.four_year_plan.current_courses.add(course)
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
        # Populate Coursework in Four Year Plan
        self.PopulateCoursework(i=0)
        self.PopulateCoursework(i=1)
        if isDataScience:
            self.PopulateCoursework(i=2)
        elif isCYBER:
            self.PopulateCoursework(i=3)
        else:
            # no particular preference for certificate program
            for i in range(4):
                self.four_year_plan.addCourse(course='ANY CSC 3000-4000', credit_hours=4)
                 
        
def main(completed_courses, find_prerequisites=False, create_four_year_plan=False, isDataScience=False, isCYBER=False, isSWE=False):
    with ChatAlgorithm(completed_courses) as chat:
        chat.cursor.execute('use thegoodadvisordb')
        
        # The User can either Find Prerequisites or Generate a Four Year Plan
        if find_prerequisites:
            return chat.FindPrerequisites(find_prerequisites)
            
        # If Generate Four Year Plan is True
        if create_four_year_plan:
            for course in completed_courses:
                chat.four_year_plan.taken_courses.add(course)
            chat.CreateFourYearPlan(isDataScience, isCYBER, isSWE)
            return chat.four_year_plan.four_year_plan
        
        chat.TheGoodAdvisor_db.commit()

# # Used for testing purposes
# if __name__ == '__main__':
#     completed_courses = set()
#     completed_courses.add('MATH 1111')
#     #completed_courses.add('MATH 1113')
#     #completed_courses.add('MATH 2211')
#     print(main(completed_courses, find_prerequisites=False, create_four_year_plan=True, isDataScience=True, isCYBER=False, isSWE=True))
    

