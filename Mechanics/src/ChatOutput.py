'''
This module is used for generic outputs in the ChatBot by using the generate four-year plan, constraints such 
as SWE, and prerequisites to be outputted.      
Author: Ashlyn Campbell 
'''
import ChatAlgorithm

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
        
        self.output = f""" I am happy to help you with your course needs! I see that you have selected to {requestType} to assist with your college journey! \n I have attached below the requested information!\n\n"""
        
    def findPrerequisite(self, completed_courses=[], find_prerequisites=[True], create_four_year_plan=False, isDataScience=False, isCYBER=False, isSWE=False):
        # returns a dictionary of prereqs
        course_prerequisites = ChatAlgorithm.main(completed_courses=completed_courses, find_prerequisites=find_prerequisites, create_four_year_plan=False, isDataScience=False, isCYBER=False, isSWE=False)
        
        self.output += f'The Prerequisites for the courses you have requested are,\n'
        
        for course in course_prerequisites.keys():
            if course_prerequisites[course]:
                prereqs = ', '.join(map(str, course_prerequisites[course]))
                self.output += f'{course} requires, {prereqs}\n'
            else:
                self.output += f'{course} does not require any prerequisites\n'
            
        return self.output
    
    def GenerateFourYearPlan(self, completed_courses=[], find_prerequisites=[], create_four_year_plan=True, isDataScience=False, isCYBER=False, isSWE=False):
        
        four_year_plan = ChatAlgorithm.main(completed_courses=completed_courses, find_prerequisites=find_prerequisites, create_four_year_plan=True, isDataScience=True, isCYBER=False, isSWE=True)
        # returns a 2d array representing the four-year plan
        
        self.output += f'The Four-Year Plan for your anticipated graduation is\n'
        for year in four_year_plan.keys():
            first_semester = ', '.join(map(str, four_year_plan[year][0]))
            second_semester = ', '.join(map(str, four_year_plan[year][1]))
            self.output += f"""{year} - \n Semester 1: {first_semester} \n Semester 2: {second_semester} \n"""
        self.output += '\n I hope this four-year plan suits your interests!'
        
        return self.output
    
# def testOutput():
    # chat = ChatOutput(findPrerequisite=True)
    # print(chat.findPrerequisite(completed_courses=[], find_prerequisites=['MATH 1111', 'MATH 1113', 'CSC 2510', 'MATH 2215']))
    
    # chat = ChatOutput(findFourYearPlan=True)
    # print(chat.GenerateFourYearPlan(completed_courses=['MATH 1111']))
# testOutput()