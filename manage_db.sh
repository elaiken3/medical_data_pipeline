#!/bin/bash

set -e  # Exit on any error

# Function to handle errors
handle_error() {
    echo "Error on line $1"
    exit 1
}

# Trap errors and call the handle_error function
trap 'handle_error $LINENO' ERR

# Arguments and Defaults
action=${1:-setup}
db_user=${DB_USER:-postgres}
db_pass=$DB_PASS
db_host=${DB_HOST:-db} 
db_port=${DB_PORT:-5432}
db_name=${DB_NAME:-medical_records}

# Function to execute psql commands with better error handling
execute_psql() {
    local command=$1
    if ! PGPASSWORD=$db_pass psql -h $db_host -p $db_port -U $db_user -d postgres -c "$command"; then
        echo "psql command failed:"
        echo "$command"
        exit 1  # Explicitly exit if psql fails
    fi
}

if [ "$action" == "setup" ]; then
    echo "Setting up database..."

    # Check if the database already exists
    if PGPASSWORD=$db_pass psql -h $db_host -p $db_port -U $db_user -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        echo "Database $db_name already exists, skipping creation"
    else
        execute_psql "CREATE DATABASE $db_name;"
    fi

    # Connect to the target database and execute the setup script
    PGPASSWORD=$db_pass psql -h $db_host -p $db_port -U $db_user -d $db_name -f setup.sql

    echo "Database setup completed."

elif [ "$action" == "teardown" ]; then
    echo "Tearing down database..."
    execute_psql "DROP DATABASE IF EXISTS $db_name;"
    echo "Database teardown completed."
else
    echo "Invalid action. Use 'setup' or 'teardown'."
    exit 1
fi
