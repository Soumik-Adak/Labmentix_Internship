use tennis;
-- competitors, competitors_rankings
-- double competitors rankings data
select * from competitors;
-- 1. Get all competitors with their rank and points
SELECT
	c.name,
    r.ranking,
    r.points
FROM competitors c 
JOIN competitor_rankings r 
	ON c.competitor_id = r.competitor_id
ORDER BY r.ranking ASC;


-- 2. Find competitors ranked in the top 5
SELECT
	c.name,
    r.ranking,
    r.points
FROM competitors c 
JOIN competitor_rankings r 
	ON c.competitor_id = r.competitor_id
WHERE r.ranking <= 5
ORDER BY r.ranking ASC;

-- 3. List competitors with no rank movement (stable rank)
SELECT
	c.name,
    r.ranking,
    r.movement
FROM competitors c 
JOIN competitor_rankings r 
	ON c.competitor_id = r.competitor_id
WHERE r.movement = 0;

-- 4. Get the total points of competitors from a specific country (e.g., Croatia)
SELECT
	c.country,
    SUM(r.points) AS total_points
FROM competitors c 
JOIN competitor_rankings r
	ON c.competitor_id = r.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

-- 5. Count the number of competitors per country
SELECT
	country,
	COUNT(competitor_id) AS competitor_count
FROM competitors
GROUP BY country
ORDER BY competitor_count DESC;

-- 6. Find competitors with the highest points in the current week
SELECT
	c.name,
    r.ranking,
    r.points
FROM competitors c 
JOIN competitor_rankings r 
	ON c.competitor_id = r.competitor_id
ORDER BY r.points DESC
LIMIT 1;
