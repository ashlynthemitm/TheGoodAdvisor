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

# Utilize course objects to view previous instances
# if pre_req set is fufilled with Course.name in other categories the student is fine
class Course:
    def __init__(self, id, course_type, course_area, course_code, course_title, credit_hours, pre_reqs):
        self.id = id
        self.course_type = course_type
        self.course_area = course_area
        self.course_code = course_code
        self.course_title = course_title
        self.credit_hours = credit_hours
        self.pre_reqs = self.createPreReqList(pre_reqs) # A 2d list containing prereqs
        
    def createPreReqList(self):
        prlist = self.pre_reqs.split(',')
        # Ex. [MATH 3302 or MATH 1111, CSC 1301]
        for index, value in enumerate(prlist):
            if 'or' in value:
                prlist[index] = value.split(' or ')
                    
        return prlist

def GetPrevCoursesInfo():
    return "SELECT * FROM CSCMajorCourses"
        
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
    
    # select columns from the database
    course_info_query = GetPrevCoursesInfo()
    cursor.execute(course_info_query)
    
    # store the course info in a variable
    course_info = cursor.fetchall() # [(id, course_type,, course_area,, course_code,, course_title, credit_hours,, pre_reqs)]
        
    # commit the changes
    TheGoodAdvisor_db.commit()
    
    # close the connection
    TheGoodAdvisor_db.close()

if __name__ == "__main__":
    main()
