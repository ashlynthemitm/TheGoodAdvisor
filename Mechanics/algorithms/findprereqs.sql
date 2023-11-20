-- Using this SQL file to find prerequisites 
-- Example: User prompts for prerequisites for CSC 1302 
/*
1. find course id for CSC 1302 in Course Table
2. use course id in prereq table to find prereqs 
3. list all prereqs, choice, prereq_course_ids (to dictate choices) 
4. send to output function to generate a response using a pre-written sentence
*/

USE thegoodadvisordb;

SELECT p.prereq_name, p.choice, p.prereq_course_id
FROM prerequisite p 
LEFT JOIN course c ON c.course_id = p.course_id
WHERE p.course_code = 'CSC 2720' -- replace the string with the variable of the prereq that is being searched
GROUP BY p.prereq_name, p.choice, p.prereq_course_id; 

-- this function can be implemented recursively to find the prereqs of each prereq 
-- continue this function tomorrow 

-- WITH RECURSIVE prerequisites AS (
--   SELECT p.prereq_name, p.choice, p.prereq_course_id
--   FROM prerequisite p 
--   LEFT JOIN course c ON c.course_id = p.course_id
--   WHERE p.course_code = 'CSC 2720' -- replace the string with the variable of the prereq that is being searched
--   UNION ALL
--   SELECT c.course_code, p.choice, p.prereq_course_id
--   FROM prerequisite p
--   JOIN prerequisite pr ON p. = pr.prereq_course_id
--   JOIN course c ON c.course_id = p.course_id
-- )
-- SELECT *
-- FROM prerequisites;