-- Data Import Command (PostgreSQL 18)
COPY Athletes FROM 'C:\Program Files\PostgreSQL\18\data\import\athletes.csv' DELIMITER ',' CSV HEADER;
COPY NOC_Regions FROM 'C:\Program Files\PostgreSQL\18\data\import\noc_regions.csv' DELIMITER ',' CSV HEADER;
COPY Events (sport, event_name, event_id) FROM 'C:\Program Files\PostgreSQL\18\data\import\events.csv' DELIMITER ',' CSV HEADER;
COPY Athlete_Events (participation_id, athlete_id, event_id, noc, year, age, height_cm, weight_kg, medal) FROM 'C:\Program Files\PostgreSQL\18\data\import\athlete_events.csv' DELIMITER ',' CSV HEADER;


-- 1. Top 10 Medaillennationen
SELECT 
    n.region_name, 
    COUNT(ae.medal) AS total_medals
FROM Athlete_Events ae
JOIN NOC_Regions n ON ae.noc = n.noc
WHERE ae.medal != 'No Medal'
GROUP BY n.region_name
ORDER BY total_medals DESC
LIMIT 10;


-- 2. Erfolgreichste Athleten nach Goldmedaillen
SELECT 
    a.name,
    COUNT(CASE WHEN ae.medal = 'Gold' THEN 1 END) AS gold_medals,
    COUNT(ae.medal) AS total_medals
FROM Athlete_Events ae
JOIN Athletes a ON ae.athlete_id = a.athlete_id
WHERE ae.medal != 'No Medal'
GROUP BY a.name
ORDER BY gold_medals DESC, total_medals DESC
LIMIT 10;


-- 3. Physische Merkmale nach Sportart (Durchschnittsgröße & -gewicht)
SELECT 
    e.sport,
    ROUND(AVG(ae.height_cm)::numeric, 1) AS avg_height_cm,
    ROUND(AVG(ae.weight_kg)::numeric, 1) AS avg_weight_kg
FROM Athlete_Events ae
JOIN Events e ON ae.event_id = e.event_id
WHERE ae.height_cm IS NOT NULL AND ae.weight_kg IS NOT NULL
GROUP BY e.sport
ORDER BY avg_height_cm DESC
LIMIT 10;