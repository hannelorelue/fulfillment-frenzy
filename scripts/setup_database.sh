#!/bin/bash

DATABASE_FILE_PATH="model/database.db"
DATABASE_LAYOUT_SQL_FILE_PATH="model/database_layout.sql"
EXAMPLE_DATA_SQL_FILE_PATH="model/example_data.sql"

# if the database file already exists delete it

if [[ -f ${DATABASE_FILE_PATH} ]]; then
    echo " * deleting existing database file at '${DATABASE_FILE_PATH}'"
    rm ${DATABASE_FILE_PATH}
fi

echo " * setup database layout in '${DATABASE_FILE_PATH}'"
sqlite3 ${DATABASE_FILE_PATH} ".read ${DATABASE_LAYOUT_SQL_FILE_PATH}"

echo " * tables created in database:"
echo "SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%'" | sqlite3 ${DATABASE_FILE_PATH}

echo " * inserting example data into database"
cat ${EXAMPLE_DATA_SQL_FILE_PATH} | sqlite3 ${DATABASE_FILE_PATH}

