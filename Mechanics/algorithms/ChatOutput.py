'''
This module is used for generic outputs in the ChatBot by using the generate four-year plan, constraints such 
as SWE, and prerequisites to be outputted.      
Author: Ashlyn Campbell 
'''
import Flask 

class ChatOutput:
    # The constructor takes in the requests the user as bool parameters and call the algorithms to place into the functions
    def __init__(self, findPrerequisite=False, findFourYearPlan=False, findSWECoursework=False):
        requestType = ''
        
        if findPrerequisite:
            requestType = 'find the Prerequisites'
        elif findFourYearPlan:
            requestType = 'find a normal Four-Year Plan'
        elif findSWECoursework:
            requestType = 'find Software Engineering Coursework within a Four-Year plan'
        else:
            print('Error no selection has been made to find output!!!')
            return
        
        self.output = f"""
        I am happy to help you with your course needs! I see that you have selected to {requestType} to assist
        with your college journey! \n
        I have attached below the requested information! \n \n
        """
        
    def findPrerequisite(self, requested_courses):
        # returns a dictionary of prereqs
        course_prerequisites = FindPreReq.main(requested_courses=requested_courses)
        
        self.output += f'The Prerequsites for the courses you have requested are,\n'
        
        for course in course_prerequisites.keys():
            prereqs = course_prerequisites[course].join(', ')
            self.output += '[{course}] requires {prereqs}'
            
        return self.output
    
    def findFourYearPlan(self, completed_courses, isDataScience=False, isCyberSecurity=False, isSWE=False):
        four_year_plan = FourYearPlan.main(completed_courses=completed_courses, isDataScience=isDataScience, isCyberSecurity=isCyberSecurity, isSWE=isSWE)
        # returns a 2d array representing the four-year plan
        
        self.output += f'The Four-Year Plan for your anticipated graduation is,'
        for year in four_year_plan.keys():
            first_semester = four_year_plan[year][0].join(', ')
            second_semester = four_year_plan[year][1].join(', ')
            output += f"""
            {year} - \n 
            Semester 1: {first_semester} \n
            Semester 2: {second_semester} \n
            """
        self.output += '\n I hope this four-year plan suits your interests!'
        
        return self.output