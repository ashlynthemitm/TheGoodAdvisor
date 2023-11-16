/* The Good Advisor Database */
-- Courses Table (Required & Not Required all stored here)
CREATE DATABASE thegoodadvisordb;
USE thegoodadvisordb;

CREATE TABLE Course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_type VARCHAR(255),
    course_area VARCHAR(10),
    course_code VARCHAR(255),
    course_title VARCHAR(255),
    credit_hours INT,
    description TEXT
);
    
-- generic Prerequisites Table (used for all Prereqs)
use thegoodadvisordb;
CREATE TABLE Prerequisite (
	prereq_id INT,
    course_id INT,
    prereq_course_id INT, -- input this value for OR prereqs
    prereq_name VARCHAR(255),
    choice BOOL,
    course_code VARCHAR(255),
    FOREIGN KEY (course_id) REFERENCES Course (course_id),
    PRIMARY KEY (course_id, prereq_id)
);


use thegoodadvisordb;








    