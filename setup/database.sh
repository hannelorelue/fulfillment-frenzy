#!/bin/bash

DATABASE_FILE_PATH="model/database.db"
DATABASE_LAYOUT_SQL_FILE_PATH="setup/database_layout.sql"
ADDRESSES_CSV_FILE_PATH="setup/addresses.csv"

# if the database file already exists delete it
if [[ -f ${DATABASE_FILE_PATH} ]]; then
    echo " * deleting existing database file at '${DATABASE_FILE_PATH}'"
    rm ${DATABASE_FILE_PATH}
fi

echo " * setup database layout in '${DATABASE_FILE_PATH}'"
duckdb ${DATABASE_FILE_PATH} ".read ${DATABASE_LAYOUT_SQL_FILE_PATH}"

echo " * tables created in database:"
duckdb ${DATABASE_FILE_PATH} "SHOW TABLES;"

echo " * inserting example data into database"
duckdb ${DATABASE_FILE_PATH} "INSERT INTO Addresses SELECT * FROM read_csv_auto('${ADDRESSES_CSV_FILE_PATH}')"

