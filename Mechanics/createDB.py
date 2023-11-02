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
        course_id INT AUTO_INCREMENT PRIMARY KEY, 
        course_type VARCHAR(50),
        course_area VARCHAR(10),
        course_code VARCHAR(10),
        course_title VARCHAR(50),
        credit_hours INT,
        description TEXT
    )
   """
    return create_coursework_query

def InputCSCMajorCoursesData():
   
    data = open('../data/TheGoodAdvisorData.xlsx')
    
    wb = xlrd.open_workbook(data)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    CoursesData = []
     
    insert_courses_query = """ INSERT INTO 
    CSCMajorCourses(course_type, course_area, course_code, course_title, credit_hours, description) VALUES (%s, %s, %s, %s, %s, %s) """
    
    # Traverse the excel sheet to input into the database
    
    for r in range(2, rows):
        tmp = (sheet.cell_value(r,0), sheet.cell_value(r,1),sheet.cell_value(r,2), sheet.cell_value(r,3), sheet.cell_value(r,4), None)
        CoursesData.append(tmp)
    
    return CoursesData, insert_courses_query

def CreatePrerequisitesTable():
    create_prerequisites_query = """

    INSERT INTO CSCMajorPrerequisites (course_id, prereq_id, course_code, can_choose)
        SELECT
            c.course_id AS course_id,
            p.prereq_id AS prereq_id,
            c.course_code AS course_code,
        0 AS can_choose
        FROM
            CSCMajorCourses c
        JOIN Prerequisites p ON c.course_code = p.course_code;

   """
    return create_prerequisites_query

def InputPrerequisitesData():
    data = open('../data/TheGoodAdvisorData.xlsx')
    
    wb = xlrd.open_workbook(data)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    CoursesData = []
     
    insert_prerequisites_query = """ INSERT INTO 
    Prerequisites(course_code, description) VALUES (%s, %s) """
    
    # Traverse the excel sheet to input into the database
    
    # update the way how i input the prereqs
    for r in range(2, rows):
        tmp = (sheet.cell_value(r,0), None)
        CoursesData.append(tmp)
    
    return CoursesData, insert_prerequisites_query
         
def CreateCSCMajorPrerequisitesTable():
    create_cscmajorprerequisites_query = """
    CREATE TABLE CSCMajorPrerequisites(
        course_id INT,  
        prereq_id INT, 
        course_code INT, 
        can_choose BIT, 
        PRIMARY KEY (course_id, prereq_id), 
        FOREIGN KEY (course_id) REFERENCES CSCMajorCourses(course_id),
        FOREIGN KEY (prereq_id) REFERENCES Prerequisites(prereq_id)
    )
   """
    return create_cscmajorprerequisites_query

def InputCSCMajorPrerequisitesData():
   
    data = open('../data/TheGoodAdvisorData.xlsx')
    
    wb = xlrd.open_workbook(data)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    CoursesData = []
    
    insert_cscmajorprerequisites_query = """
    INSERT INTO CSCMajorPrerequisites (course_id, prereq_id, course_code, can_choose)
    SELECT
        c.course_id AS course_id,
        p.prereq_id AS prereq_id,
        c.course_code AS course_code,
        0 AS can_choose
    FROM
        CSCMajorCourses c
    JOIN Prerequisites p ON c.course_code = p.course_code;
    """

    return insert_cscmajorprerequisites_query
  
def UpdateCanChooseAttribute(): 
    
    data = open('../data/TheGoodAdvisorData.xlsx')
    
    wb = xlrd.open_workbook(data)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    
    choose_codes = []
    
    for r in range(2,rows):
        prereqs = sheet.cell_value(r,5).split(',')
        for p in prereqs:
            if 'or' in p:
                choices = p.split(' or ')
                choose_codes.extend(choices)
                
    return choose_codes           
            
   
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

        # create tables
        cursor.execute(CreateCSCMajorCoursesTable())
        cursor.execute(CreatePrerequisitesTable())
        cursor.execute(CreateCSCMajorPrerequisitesTable())

        # input data
        data_to_insert, insert_data_query = InputCSCMajorCoursesData()
        for record in data_to_insert:
            cursor.execute(insert_data_query, record)

        data_to_insert, insert_data_query = InputPrerequisitesData()
        for record in data_to_insert:
            cursor.execute(insert_data_query, record)

        insert_data_query = InputCSCMajorPrerequisitesData()
        cursor.execute(insert_data_query)

        # update the can choose element using the excel sheet
        choose_codes = UpdateCanChooseAttribute()
        
        for code in choose_codes:
            update_choice_query = f"""
            UPDATE CSCMajorPrerequisites
            SET can_choose = 1
            WHERE course_code = {code};
            """
            cursor.execute(update_choice_query)
        
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
