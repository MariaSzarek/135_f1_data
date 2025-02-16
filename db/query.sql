create database f1db;
use f1db;

show create table circuits;
desc circuits;
desc constructorresults;

SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'circuits' AND CONSTRAINT_NAME <> 'PRIMARY';

SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'driverstandings';

select * from driverstandings order by driverStandingsId desc limit 30;
select * from races where raceId = 1144;
select * from constructorstandings where raceId= 1144 order by position;

select * from races where year=2024;

select * from circuits;
select * from results where raceId=1124 order by position;

select results.raceId, results.position, drivers.surname
from results
inner join drivers on results.driverId = drivers.driverId
inner join races on results.raceId = races.raceId
where drivers.surname IN ("Alonso", "Stroll") and  races.year >2023
order by results.raceId, results.position; 


SELECT 
    r.raceId, 
    alonso.position AS alonso_position, 
    stroll.position AS stroll_position, 
    CASE 
        WHEN COALESCE(alonso.position, 21) < COALESCE(stroll.position, 21) THEN 1 
        ELSE 0 
    END AS alonso_better_than_stroll
FROM races r
LEFT JOIN results alonso ON r.raceId = alonso.raceId 
    AND alonso.driverId = (SELECT driverId FROM drivers WHERE surname = 'Alonso')
LEFT JOIN results stroll ON r.raceId = stroll.raceId 
    AND stroll.driverId = (SELECT driverId FROM drivers WHERE surname = 'Stroll')
WHERE r.year > 2023
ORDER BY r.raceId;

desc drivers;





