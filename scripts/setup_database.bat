@echo off

SET DATABASE_FILE_PATH=".\\model\\database.db"
SET DATABASE_LAYOUT_SQL_FILE_PATH=".\\model\\database_layout.sql"
SET EXAMPLE_DATA_SQL_FILE_PATH=".\\model\\example_data.sql"

:: if the database file already exists delete it
IF EXIST %DATABASE_FILE_PATH% (
	echo * deleting existing database file at '%DATABASE_FILE_PATH%'
	DEL /F %DATABASE_FILE_PATH%
)

echo * setup database layout in '%DATABASE_FILE_PATH%
duckdb %DATABASE_FILE_PATH% ".read %DATABASE_LAYOUT_SQL_FILE_PATH%"

echo * tables created in database:
duckdb %DATABASE_FILE_PATH% "SHOW TABLES;"

echo * inserting example data into database
duckdb %DATABASE_FILE_PATH% ".read %EXAMPLE_DATA_SQL_FILE_PATH%"

