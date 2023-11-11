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
        self.priority_stack = ['Core Curriculum', 'Major Requirements', 'Certificate']
        self.completed_courses = set()
        # queues for courses to take order (will include prerequisite shifting)
        self.core_courses = []
        self.major_courses = []
        self.certificate = []
        self.four_year_plan = [[[], []], [[], []], [[], []], [[], []]]
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
            SELECT c.course_code, c.course_title, c.credit_hours
            FROM Course c
            WHERE c.course_type = '{self.priority_stack[i]}';
            GROUP BY c.course_code, c.course_title, c.credit_hours;
        """
        
        return find_priority_query
       
def main(completed_courses):
    with DeterminePlan(completed_courses) as dp:
        dp.cursor.execute('use thegoodadvisordb')
        
        # Look for Core Requirements first
        find_priority_query = dp.priorityFunc(0) 
        dp.cursor.execute(find_priority_query)
        
        results = dp.cursor.fetchall() # each row contains: course_code, course_title, credit_hours
        choices = {} # {prereq_course_id: index}
        
        '''
        Nexts steps: Add a Not in Clause for the core_classes, adjust determination
        for adding courses in --> courses overlap with prereqs so primarily use for 
        considering adding something new
        '''
        
        for row in results: 
            course_code, course_title, credit_hours = row
        
            # find the best order to take Core Requirements
            if course_code not in completed_courses: 
                prereqs = FindPreReq.main(course_code) # get prereq info
                
                for p in prereqs: # adding prereqs before original courses
                    if p.course_code in completed_courses:
                        continue # move to the next prerequsite
                    if p.choice:
                        if p.prereq_course_id not in choices.keys():
                            dp.core_courses.append(p.prereq_name)
                            choices[p.prereq_course_id] = dp.core_courses.index(p.prereq_name)
                        else:
                            choiceIndex = choices[p.prereq_course_id]
                            dp.core_courses[choiceIndex] += ' or ' + p.prereq_name
                    else:
                        dp.core_courses.append(p.prereq_name)
                        
                dp.core_courses.append(course_code) # add course once prereqs are in
                
            else:
                continue # course has been completed move to the next course
        
        
        dp.TheGoodAdvisor_db.commit()
        print(dp.core_courses)


if __name__ == '__main__':
    print(main(completed_courses=['MATH 1111', 'MATH 1113'])) # printing for now, the dictionary needs to be returned to the calling class