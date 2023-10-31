'''
Create the Database System using MySQL 
Author: Ashlyn Campbell 

'''
import mysql.connector
from dotenv import load_dotenv
import xlrd
import os

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
    
    # create tables
   
    # input data iteratively
    # data_to_insert, insert_data_query = function()
    # for record in data_to_insert:
    #     cursor.execute(insert_data_query, record)
    
    
    # commit the changes
    TheGoodAdvisor_db.commit()
    
    # close the connection
    TheGoodAdvisor_db.close()

if __name__ == "__main__":
    main()
