#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error on line $1"
    exit 1
}

# Trap errors and call the handle_error function
trap 'handle_error $LINENO' ERR

# Arguments
action=$1
db_user="postgres"
db_pass=$2
db_name="medical_records"

# Function to execute psql commands and handle errors
execute_psql() {
    local command=$1
    PGPASSWORD=$db_pass psql -U $db_user -d postgres -c "$command"
}

if [ "$action" == "setup" ]; then
    echo "Setting up database..."
    execute_psql "DROP DATABASE IF EXISTS $db_name;"
    execute_psql "CREATE DATABASE $db_name;"
    PGPASSWORD=$db_pass psql -U $db_user -d $db_name -f setup.sql
    echo "Database setup completed."
elif [ "$action" == "teardown" ]; then
    echo "Tearing down database..."
    execute_psql "DROP DATABASE IF EXISTS $db_name;"
    echo "Database teardown completed."
else
    echo "Invalid action. Use 'setup' or 'teardown'."
    exit 1
fi

