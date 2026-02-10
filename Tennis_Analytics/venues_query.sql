use tennis;
-- complexes, venues
-- complexes data
-- 1. List all venues along with their associated complex name
SELECT
	v.venue_name,
    c.complex_name
FROM venues v 
JOIN complexes c 
	ON v.complex_id = c.complex_id;


-- 2. Count the number of venues in each complex
SELECT
	c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM venues v 
JOIN complexes c 
	ON v.complex_id = c.complex_id
GROUP BY c.complex_name
ORDER BY venue_count DESC;


-- 3. Get details of venues in a specific country (e.g., Chile)
SELECT 
	v.venue_name,
    v.city_name,
    v.country_name,
    v.country_code,
    v.timezone,
    c.complex_name
FROM venues v 
JOIN complexes c 
	ON v.complex_id = c.complex_id
WHERE country_name = "CHILE";


-- 4. Identify all venues and their timezones
SELECT
	venue_name,
    timezone
FROM venues;


-- 5. Find complexes that have more than one venue
SELECT
	c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM venues v 
JOIN complexes c 
	ON v.complex_id = c.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id)>1;


-- 6. List venues grouped by country
SELECT
	country_name,
	COUNT(venue_id) as venue_count
FROM venues
GROUP BY country_name
ORDER BY venue_count DESC;


-- 7. Find all venues for a specific complex (e.g., Nacional)
SELECT
	v.venue_name,
    v.country_name,
    v.city_name,
    v.country_code,
    v.timezone
FROM venues v 
JOIN complexes c 
	ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';
    
    