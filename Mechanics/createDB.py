'''
Create the Database System using MySQL 
Author: Ashlyn Campbell 

Future Steps: Create a table for non-major requirements
'''
import mysql.connector
from dotenv import load_dotenv
import xlrd
import os

def CreateCourseTable():
    create_coursework_query = """
    CREATE TABLE Course (
        course_id INT AUTO_INCREMENT PRIMARY KEY,
        course_type VARCHAR(50),
        course_area VARCHAR(10),
        course_code VARCHAR(10),
        course_title VARCHAR(50),
        credit_hours INT,
        description TEXT
    );
   """
    return create_coursework_query

def CreatePrerequisiteTable():
    create_prerequisites_query = """

    CREATE TABLE Prerequisite (
	    prereq_id INT,
        course_id INT,
        prereq_course_id INT, 
        prereq_name VARCHAR(255),
        choice BOOL,
        course_code VARCHAR(255),
        FOREIGN KEY (course_id) REFERENCES Course (course_id),
        PRIMARY KEY (course_id, prereq_id)
    );

   """
    return create_prerequisites_query

def InputTableData():
    
    wb = xlrd.open_workbook('C:\\Users\\ashly\\OneDrive\\Documents\\Education Material\\SWEClass\\ProjectRepo\\TheGoodAdvisor\\Mechanics\\data\\TheGoodAdvisorData.xls')
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    
    PrerequisitesData = []

    insert_prerequisites_query = """ INSERT INTO 
    Prerequisite(prereq_id, course_id, prereq_course_id, prereq_name, choice, course_code) VALUES (%s, %s, %s, %s, %s, %s); """
    
    course_id = 1
    prereq_id = 1
    prereq_course_id = 1
    
    for r in range(1, rows):
        if course_id > 33:
            break
        course_code = sheet.cell_value(r,2)
        if (sheet.cell_value(r,5)) == '':
            continue # no prereq
        
        prereq_arr = (sheet.cell_value(r,5)).split(',')
        for prereq in prereq_arr:
            if 'or' in prereq:
                choices = prereq.split(' or ')
                for choice in choices:
                    tmp = (prereq_id, course_id, prereq_course_id, choice, True, course_code)
                    PrerequisitesData.append(tmp)
                    prereq_id += 1
            else:
                tmp = (prereq_id, course_id, prereq_course_id, prereq, False, course_code)
                PrerequisitesData.append(tmp)
                prereq_id += 1
                prereq_course_id += 1
            
        prereq_course_id += 1
        course_id += 1
    
    return PrerequisitesData, insert_prerequisites_query

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
        
        # create tables
        # cursor.execute(CreateCourseTable())
        # cursor.execute(CreatePrerequisiteTable())

        # input data
        data_to_insert, insert_data_query = InputTableData()
        for record in data_to_insert:
            cursor.execute(insert_data_query, record)
            
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
