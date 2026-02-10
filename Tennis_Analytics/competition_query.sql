use tennis;
-- categories, competitions
-- Competitions data 
-- 1. List all competitions along with their category name
SELECT 
	c.competition_name, 
    cat.category_name
FROM competitions c 
JOIN categories cat 
	ON c.category_id = cat.category_id;
    
-- 2. Count the number of competitions in each category
SELECT 
	cat.category_name, 
    COUNT(c.competition_id) AS competition_count
FROM competitions c 
JOIN categories cat 
	ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY competition_count DESC;
    

-- 3. Find all competitions of type 'doubles'
SELECT competition_name, type, gender
FROM competitions
WHERE type ='doubles';

-- 4. Get competitions that belong to a specific category (e.g., ITF Men)
SELECT 
	c.competition_name, 
    c.type, 
    c.gender
FROM competitions c 
JOIN categories cat 
	ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';


-- 5. Identify parent competitions and their sub-competitions
SELECT 
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM competitions child
JOIN competitions parent
    ON child.parent_id = parent.competition_id
ORDER BY parent_competition;


-- 6. Analyze the distribution of competition types by category
SELECT
	cat.category_name,
    c.type AS competition_type,
    COUNT(*) AS competition_count
FROM competitions c 
JOIN categories cat 
	ON c.category_id = cat.category_id
GROUP BY
	cat.category_name,
    c.type
ORDER BY
	cat.category_name,
    competition_count DESC;

-- 7. List all competitions with no parent (top-level competitions)
SELECT
	competition_name, 
    type,
    gender
FROM competitions
WHERE parent_id IS NULL;
