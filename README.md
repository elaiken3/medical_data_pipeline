Medical Data Processing Pipeline
================================

This project involves creating a data pipeline to clean and process medical records from various CSV files and load them into a PostgreSQL database. Additionally, it includes feature engineering to prepare the data for machine learning models or analytics. The pipeline also includes a Flask API to access the processed data and calculated features securely using JWT authentication.

Steps in the Pipeline
---------------------

### 1\. Data Cleaning and Feature Engineering

**DataCleaner Class:**

-   Initializes by loading data from a given CSV file.
-   Removes duplicates and handles missing values by flagging them.

**LifestyleCleaner Class:**

-   Inherits from `DataCleaner`.
-   Adds date standardization specific to the `report_date` column.

**RxCleaner Class:**

-   Inherits from `DataCleaner`.
-   Standardizes the `rx_date` column and the `rx_norm` column to uppercase.
-   Adds a feature to indicate if the patient is taking alpha blockers.

**ConditionsCleaner Class:**

-   Inherits from `DataCleaner`.
-   Adds date standardization specific to the `report_date` column.

**LabsCleaner Class:**

-   Inherits from `DataCleaner`.
-   Standardizes the `feature_date` column.
-   Converts the `value` column to numeric.
-   Adds features for the most recent Hemoglobin (HGB) and A1c readings and counts high cholesterol events.

**TestsCleaner Class:**

-   Inherits from `DataCleaner`.
-   Standardizes the `report_date` column.
-   Adds features for average systolic and diastolic blood pressure.

### 2\. Execute Bash Scripts for Database Setup and Teardown

**execute_bash_script Function:**

-   Executes a bash script (`manage_db.sh`) to set up or tear down the database.
-   Handles errors and logs the output.

### 3\. Load Data into Database

**load_data Function:**

-   Loads cleaned and processed data into the specified table in the PostgreSQL database.
-   Uses SQLAlchemy for database interactions.

### 4\. Run the Pipeline

**main Function:**

-   Initializes and cleans data from each CSV file using the appropriate cleaner class.
-   Executes the database setup script.
-   Loads the cleaned data into the respective tables in the PostgreSQL database.
-   Optionally, executes the database teardown script.

### 5\. Flask API with JWT Authentication

**Flask API:**

-   Provides endpoints to access the processed data and calculated features for each patient.
-   Uses JWT for secure access.

Instructions for Running the Pipeline
-------------------------------------

### Prerequisites

1.  Install the required Python libraries:

    ```
    pip install pandas numpy psycopg2 sqlalchemy flask flask-jwt-extended
    ```

3.  Set up PostgreSQL and create a user with appropriate permissions.

### Steps to Run the Pipeline

1.  **Modify the database connection parameters in the pipeline script (`pipeline.py`):**

    ```DB_NAME = "medical_records"
    DB_USER = "postgres"
    DB_PASS = "your_password"  # Replace with your actual password
    DB_HOST = "localhost"
    DB_PORT = "5432"
    ```
2.  **Run the pipeline script:**

    ```
    python3 pipeline.py
    ```
    
3.  **Start the Flask API:**

    ```
    python3 api.py
    ```

### Example Usage

1.  **Login to Get a Token:**

    ```
    curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username":"test", "password":"test"}'
    ```

    This should return a JSON response with the access token.

3.  **Access Processed Data:**

    ```
    curl -X GET http://127.0.0.1:5000/person/1 -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
    ```

    Replace `YOUR_ACCESS_TOKEN` with the token received from the login response.

5.  **Access Calculated Features:**

    ```
    curl -X GET http://127.0.0.1:5000/person/1/features -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
    ```

    Replace `YOUR_ACCESS_TOKEN` with the token received from the login response.

