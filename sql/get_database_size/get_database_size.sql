SELECT 
SUM(round(((data_length + index_length) / 1024 / 1024), 2)) AS `mb` 
FROM information_schema.TABLES 
WHERE table_schema = "erpsim_games";