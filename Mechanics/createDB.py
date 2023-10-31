'''
Create the Database System using MySQL 
Author: Ashlyn Campbell 

Future Steps: Create a table for non-major requirements
'''
import mysql.connector
from dotenv import load_dotenv
import xlrd
import os

def CreateCSCMajorCoursesTable():
    create_coursework_query = """
    CREATE TABLE CSCMajorCourses(
        id INT AUTO_INCREMENT PRIMARY KEY, 
        course_type VARCHAR(50),
        course_area VARCHAR(10),
        course_code VARCHAR(10),
        course_title VARCHAR(50)
        credit_hours INT,
        pre_reqs VARCHAR(255)
    )
   """
   
    '''
    The pre_reqs value can be adapted into a separate table instead of this string, for now it can be split using the 'or' and ',' values.
    '''
    return create_coursework_query

def InputCSCMajorCoursesData():
   
    data = open('data/TheGoodAdvisorData.xlsx')
    
    wb = xlrd.open_workbook(data)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    CoursesData = []
     
    insert_courses_query = """ INSERT INTO 
    CSCMajorCourses(course_type, course_area, course_code, course_title, credit_hours, pre_reqs) VALUES (%s, %s, %s, %s, %s, %s) """
    
    # Traverse the excel sheet to input into the database
    
    for r in range(2, rows):
        tmp = (sheet.cell_value(r,0), sheet.cell_value(r,1),sheet.cell_value(r,2), sheet.cell_value(r,3), sheet.cell_value(r,4), sheet.cell_value(r,5))
        CoursesData.append(tmp)
    
    return CoursesData, insert_courses_query
   
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
    
    # using this cursor to input data
    cursor = TheGoodAdvisor_db.cursor() 
    
    # create CSCMajorCoursework table
    cursor.execute(CreateCSCMajorCoursesTable())
    
    # input restaurant data
    data_to_insert, insert_data_query = InputCSCMajorCoursesData()
    for record in data_to_insert:
        cursor.execute(insert_data_query, record)
        
    # commit the changes
    TheGoodAdvisor_db.commit()
    
    # close the connection
    TheGoodAdvisor_db.close()

if __name__ == "__main__":
    main()
