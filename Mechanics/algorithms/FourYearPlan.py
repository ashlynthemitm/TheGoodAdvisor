'''
Four Year Plan Algorithm based on previous input of previous coursework or 0 credits.
Author: Ashlyn Campbell 
'''
import mysql.connector
from dotenv import load_dotenv
import os 

class DeterminePlan():
    
    def __init__(self, completed_courses):
        self.priority_stack = ['Core Curriculum', 'Major Requirements', 'Certificate']
        self.completed_courses = set()
        self.four_year_plan = [[[], []], [[], []], [[], []], [[], []]]
        
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
            SELECT c.course_code, c.course_title, c.course_type, c.credit_hours
            FROM Course c
            WHERE c.course_type = '{self.priority_stack[i]}';
            GROUP BY c.course_code, c.course_title, c.credit_hours;
        """
        
        return find_priority_query
       
def main(completed_courses):
    with DeterminePlan(completed_courses) as dp:
        dp.cursor.execute('use thegoodadvisordb;')
        
        dp.cursor.execute()
        dp.TheGoodAdvisor_db.commit()


if __name__ == '__main__':
    print(main(completed_courses=['MATH 1111', 'MATH 1113'])) # printing for now, the dictionary needs to be returned to the calling class