#!/bin/bash

DATABASE_FILE_PATH="model/database.db"

# if the database file already exists delete it

if [[ -f ${DATABASE_FILE_PATH} ]]; then
    echo " * deleting existing database file at '${DATABASE_FILE_PATH}'"
    rm ${DATABASE_FILE_PATH}
fi

echo " * setup database layout in '${DATABASE_FILE_PATH}'"
sqlite3 ${DATABASE_FILE_PATH} ".read model/database_layout.sql"
