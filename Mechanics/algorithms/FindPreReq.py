'''
PreRequisite of Courses algorithm to utilize for any questions related to classes able to take.

Author: Ashlyn Campbell 
'''

'''
Steps: 

1. Select columns from database --> pre-reqs, course code, course title, course type

Algorithm mechanics --> prioritize type first (CORE > MAJOR > CERTIFICATE)

place previous taken courses in set --> compare set to any courses planning to add to queue
'''
import mysql.connector
from dotenv import load_dotenv
import os 


def findCoursePrerequsite(course):
    '''
    if a user requests the prerequsites for a course this function will output that data
    '''

def main():
    load_dotenv() # creation of .env file to store mysql credentials 
    host_db = os.getenv('DB_HOST')
    username_db = os.getenv('DB_USERNAME')
    password_db = os.getenv('DB_PASSWORD')
    TheGoodAdvisor_db = mysql.connector.connect(
        host=host_db,
        user=username_db,
        password=password_db
    )
    
    try: 
        
        # using this cursor to input data
        cursor = TheGoodAdvisor_db.cursor() 
        cursor.execute('use thegoodadvisordb;')

        # input data
            
        # commit the changes
        TheGoodAdvisor_db.commit()
        
    except mysql.connector.Error as error:
        # Handle errors
        print(f'Error: {error}')
    
    finally:
        # close the cursor and database connection
        cursor.close()
        TheGoodAdvisor_db.close()
        

if __name__ == "__main__":
    main()
