# The Good Advisor

## Table of Contents
- [Description](#description)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Sprint 1 Presentation](#sprint-1-presentation)
- [Sprint 2 Presentation](#sprint-2-presentation)
- [Test Cases](#test-cases)

## Description
The GoodAdvisor is a selection input-based Chatbot created to assist Computer Science students with choosing the correct coursework to take. Picking schedules is hard for anybody, but for CS students it can be difficult to know the best path to take, to effectively prepare for the next one and internships. This way students can map out their four years of college efficiently and intentionally. Students will be prompted with questions to satisfy their user story and have the chance to check off any course they have already taken. 

## Functional Requirements

1. Course Recommendation: The system must provide course recommendations based on a user's academic progress, major, and career goals.
2. Generating Schedules: The Good Advisor should generate a comprehensive, semester-by-semester course schedule for users, taking into account course prerequisites.
3. Natural Language Chatbot: The chatbot must understand and respond to natural language queries related to course selection, prerequisites, and academic planning.
4. Internship and Career Guidance: The chatbot should provide information and resources related to internships, co-op programs, and career opportunities in computer science.
5. Semester Load Analysis: The chatbot should help users maintain a balanced semester course load, considering credit hours, workload, and the importance of specific courses.

## Non-Functional Requirements
    
1. Usability and User Experience: The web application must have an intuitive and user-friendly interface to cater to a diverse user base.
2. Compatibility and Browser Support: The web application should be compatible with a wide range of browsers and devices, ensuring accessibility for all users.
3. Interoperability: If the chatbot integrates with external systems or databases, it should ensure smooth interoperability and data exchange with those systems.
4. Comprehensive Testing: Thorough testing, including unit testing, integration testing, and user acceptance testing, should be conducted to ensure the chatbot's reliability and functionality.
5. Response Language and Tone: It should adapt its language and tone to be informative and supportive, catering to the educational context.


## Sprint 1 Presentation
https://docs.google.com/presentation/d/1yGV_tC4jtSiPHOuWyx7I7WPqB9XT_VjyeSi4KRjJuy0/edit?usp=sharing

## Sprint 2 Presentation
https://docs.google.com/presentation/d/10QOdjy4xlSK6FF20TBklw_5hjoAbyHpOHBGpCyHEKLQ/edit?usp=sharing

## Test Cases 

1. User asks about internship opportunities in computer science and the chatbot offers relevant information and resources.

    a. Pass: The chatbot provides correct information about possible internships.

    b. Fail: The chatbot provides outdated or irrelevant internship information.

2. User specifies a major and career goals and the chatbot recommends a relevant set of courses.

    a. Pass: Recommended courses align with the major and career goals.

    b. Fail: Chatbot offers courses that they’ve already taken and does not outline           with career goals or major goals.

3. User inputs their desired semester course load and preferences and the chatbot suggests a balanced course load.

    a. Pass: The suggested course load is balanced and fits the user's preferences.

    b. Fail: The suggested course load does not align with user’s preferences.

4. The chatbot interacts with an external database for course information and the data exchange between the chatbot and the database is smooth.

    a. Pass: Data is correctly iterated to the chatbot output to find the correct             solution.

    b. Fail: The chatbot encounters data retrieval or update errors.

5. User wants to enroll in a course without the necessary prerequisites and the

    a. Pass: Chatbot informs the user about the missing prerequisites.

    b. Fail: The Chatbot fails to recognize the prerequisites or provides incorrect         information.

6. User selects question prompts.

    a. Pass: The prompt is collected.

    b. Fail: The prompt was selected but no data was stored.

7. Users access the web application using mobile devices and the web application adapts to mobile screens for optimal user experience.

    a. Pass: The application's layout and functionality are responsive on mobile             devices.

    b. Fail: The mobile version of the web application is difficult to navigate or           has display issues.

8. Users interact with the Chatbot for rapid responses and the Chatbot responds promptly to user queries.

    a. Pass: The Chatbot provides quick and responsive answers.

    b. Fail: The Chatbot exhibits slow response times.

9. When many users are interacting with the Chatbot simultaneously for an extended period.

    a. Pass: The Chatbot remains responsive and reliable under prolonged heavy usage.

    b. Fail: The Chatbot's performance deteriorates under prolonged stress.

10. Simulate system maintenance and updates and the Chatbot should gracefully handle maintenance, with minimal downtime.

    a. Pass: The Chatbot's maintenance activities are carried out without significant         disruption to users.

    b. Fail: The Chatbot experiences extended downtime or issues during maintenance.




