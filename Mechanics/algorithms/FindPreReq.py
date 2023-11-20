'''
PreRequisite of Courses algorithm to utilize for any questions related to classes able to take.

Author: Ashlyn Campbell 
'''
import mysql.connector
from dotenv import load_dotenv
import os 
from collections import namedtuple

class FindPrerequsites:
    Prerequisite = namedtuple('Prerequisite', ['prereq_name', 'choice', 'prereq_course_id', 'course_title'])
    
    def __init__(self):
        self.temp = None

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

    def findCoursePrerequsite(self, course):
        find_prereq_query = f"""
            SELECT p.prereq_name, p.choice, p.prereq_course_id, c.course_code, c.course_title
            FROM prerequisite p 
            LEFT JOIN course c ON c.course_id = p.course_id
            WHERE p.course_code = '{course}'
            GROUP BY p.prereq_name, p.choice, p.prereq_course_id, c.course_code, c.course_title, c.credit_hours;
            """
        return find_prereq_query
    
def main(requested_courses): # The list Prerequisites section will use the Main to get a dictionary of Prerequisites
    with FindPrerequsites() as fp:
        fp.cursor.execute('use thegoodadvisordb')
        results = []
        for course in requested_courses: # update in the future to find all prerequsites 
            fp.cursor.execute(fp.findCoursePrerequsite(course))
            results.extend(fp.cursor.fetchall())
            course_prerequisites = {}
            
        for row in results:
            prereq_name, choice, prereq_course_id, course_code, course_title = row
            prereq = fp.Prerequisite(prereq_name, choice, prereq_course_id, course_title)
            if course_code in course_prerequisites:
                course_prerequisites[course_code].append(prereq)
            else:
                course_prerequisites[course_code] = [prereq]

        fp.TheGoodAdvisor_db.commit()

        return course_prerequisites
        
if __name__ == '__main__':
    print(main(['CSC 1301'])) # printing for now, the dictionary needs to be returned to the calling class
