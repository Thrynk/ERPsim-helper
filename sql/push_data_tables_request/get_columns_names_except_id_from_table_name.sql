SELECT 
column_name
FROM 
information_schema.columns 
WHERE TABLE_SCHEMA = "erpsim_games"
AND table_name = "inventory"
AND column_key <> "PRI";