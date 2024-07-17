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

Containerization with Docker
----------------------------

This project is designed to run within Docker containers for easy deployment and reproducibility. Here's how to get started:

**Prerequisites:**

-   Docker and Docker Compose installed on your system.

**Steps:**

1.  **Obtain `wait-for-it.sh` Script:**

    -   Download the script from its GitHub repository:

        Bash

        ```
        wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh

        ```


    -   Place the `wait-for-it.sh` file in your project's root directory (same level as `docker-compose.yml`).
    -   Make it executable:

        Bash

        ```
        chmod +x wait-for-it.sh

        ```

2.  **Define the Environment:**

    -   Create a `.env` file to store your database credentials (`DB_NAME`, `DB_USER`, `DB_PASS`) and `JWT_SECRET_KEY`.
    -   Ensure the correct values are set for `DB_HOST` and `DB_PORT` in your `pipeline.py` script, reflecting the Docker configuration.
3.  **Build and Run with Docker Compose:**

    -   Open a terminal in the project directory.
    -   Run `docker-compose up --build`. This will build the Docker images for your application and PostgreSQL database, create containers, and start them.
    -   The first run might take a while as it downloads the necessary images and builds the application.

**Accessing the API After Deployment:**

-   Once the containers are running, your Flask API should be accessible at `http://localhost:5001`.
-   You can interact with it using tools like `curl`, a web browser, or a Python script.
-   Remember that the `/person/<person_id>` and `/person/<person_id>/features` endpoints require JWT authentication, so you'll need to get a token from the `/login` endpoint first.

**Example Usage (with curl):**

Bash

```
# Login to get a token
curl -X POST http://localhost:5001/login -H "Content-Type: application/json" -d '{"username":"test", "password":"test"}'

# Access processed data
curl -X GET http://localhost:5001/person/1 -H "Authorization: Bearer <your_access_token>"

# Access calculated features
curl -X GET http://localhost:5001/person/1/features -H "Authorization: Bearer <your_access_token>"

```

* * * * *

**(Optional) Instructions for Running the Pipeline Locally (without Docker)**

1.  Install the required Python libraries:

    Bash

    ```
    python -m venv venv
    source venv/bin/activate
    pip install pandas numpy psycopg2 sqlalchemy flask flask-jwt-extended

    ```


2.  Set up PostgreSQL and create a user with appropriate permissions.

3.  Modify the database connection parameters in the `.env` file:

    ```
    DB_NAME=medical_records
    DB_USER=postgres
    DB_PASS=your_password  # Replace with your actual password

    ```

4.  Run the pipeline script:

    Bash

    ```
    python3 pipeline.py

    ```

5.  Start the Flask API:

    Bash

    ```
    python3 api.py

    ```

### Database Schema Diagram ###

#### 1. lifestyle
- **impairment_category**: VARCHAR(255)
- **impairment**: VARCHAR(255)
- **lifestyle_category**: VARCHAR(255)
- **feature_type**: VARCHAR(255)
- **feature**: VARCHAR(255)
- **report_date**: DATE
- **clinician_specialty**: VARCHAR(255)
- **value**: VARCHAR(255)
- **secondary_value**: VARCHAR(255)
- **person_id**: INT
- **impairment_missing**: INT
- **value_missing**: INT
- **secondary_value_missing**: INT

#### 2. rx
- **impairment_category**: VARCHAR(255)
- **impairment**: VARCHAR(255)
- **din**: VARCHAR(255)
- **rx_name**: VARCHAR(255)
- **rx_type**: VARCHAR(255)
- **start_date**: DATE
- **end_date**: DATE
- **rx_date**: DATE
- **rx_norm**: VARCHAR(255)
- **person_id**: INT
- **impairment_category_missing**: INT
- **impairment_missing**: INT
- **din_missing**: INT
- **rx_type_missing**: INT
- **end_date_missing**: INT
- **rx_norm_missing**: INT
- **taking_alpha_blockers**: BOOLEAN

#### 3. conditions
- **id**: INT
- **impairment_category**: VARCHAR(255)
- **impairment**: VARCHAR(255)
- **feature_type**: VARCHAR(255)
- **feature**: VARCHAR(255)
- **icd_code**: VARCHAR(255)
- **report_date**: DATE
- **clinician_specialty**: VARCHAR(255)
- **value**: VARCHAR(255)
- **person_id**: INT
- **impairment_category_missing**: INT
- **impairment_missing**: INT
- **icd_code_missing**: INT
- **value_missing**: INT

#### 4. labs
- **impairment_category**: VARCHAR(255)
- **impairment**: VARCHAR(255)
- **feature_type**: VARCHAR(255)
- **loinc**: VARCHAR(255)
- **feature_date**: DATE
- **feature**: VARCHAR(255)
- **value**: VARCHAR(255)
- **normal_range_of_value**: VARCHAR(255)
- **result_evaluation_or_flag**: VARCHAR(255)
- **person_id**: INT
- **impairment_missing**: INT
- **normal_range_of_value_missing**: INT
- **result_evaluation_or_flag_missing**: INT
- **most_recent_hgb**: FLOAT
- **most_recent_a1c**: FLOAT
- **high_cholesterol_events**: INT

#### 5. tests
- **impairment_category**: VARCHAR(255)
- **impairment**: VARCHAR(255)
- **feature_type**: VARCHAR(255)
- **feature**: VARCHAR(255)
- **icd_code**: VARCHAR(255)
- **report_date**: DATE
- **value**: VARCHAR(255)
- **person_id**: INT
- **impairment_category_missing**: INT
- **impairment_missing**: INT
- **icd_code_missing**: INT
- **value_missing**: INT
- **average_systolic_bp**: INT
- **average_diastolic_bp**: INT

#### Relationships
- **person_id**: INT
  - This column is present in the `lifestyle`, `rx`, `conditions`, `labs`, and `tests` tables.
  - It is used to link records in these tables to a specific person.



### Discussion Point #1: Handling Data from Different Vendors

#### 1\. Receive the Data from Vendors

To handle data from various vendors efficiently and securely, consider the following approaches:

-   **API Endpoints**: Set up secure RESTful API endpoints where vendors can post JSON files. Ensure that these endpoints have proper authentication and authorization mechanisms to prevent unauthorized access.

#### 2\. Ingest the Data into Our Database

Once the data is received, the next step is to ingest it into the database efficiently:

-   **Batch Processing**: Collect the JSON files into batches and process them together. This reduces the overhead of frequent database connections and can be scheduled during off-peak hours.

#### 3\. Minimize Table Locking During Data Ingestion

To minimize table locking and ensure the database remains responsive during data ingestion:

-   **Partitioning**: Partition the tables based on logical keys such as `person_id` or date. This reduces contention and allows parallel processing of different partitions.
-   **Bulk Inserts**: Use bulk insert operations instead of individual row inserts. This reduces the number of transactions and locks held on the table.

#### 4\. Best Database for This Data

Considering the nature and volume of the data, a combination of databases might be the best approach:

-   **Relational Databases**: Relational databases like PostgreSQL, MySQL or Oracle would probably best for storing structured data that requires complex queries and transactions. 


### Discussion Point #2: Deploying to a Cloud Environment

#### Recommended Cloud Provider and Services

For deploying the medical data processing pipeline and API service, I recommend using Google Cloud Platform (GCP) due to its comprehensive suite of services and robust support for data processing, storage, and machine learning. Here's how you can deploy the solution on GCP:

1.  **Google Cloud Storage (GCS)**:

    -   Use GCS buckets to store incoming JSON files from vendors securely.
    -   Set up event notifications for GCS buckets to trigger processing when new files are uploaded.

2.  **Google Cloud Pub/Sub**:

    -   Use Pub/Sub for real-time data ingestion and processing. This helps in decoupling and scaling the data processing pipeline.

3.  **Google Cloud Functions**:

    -   Use Cloud Functions to run pipeline script in conjunction with a Pub/Sub trigger for an event-driven architecture.

4. **Google Cloud Run**:

    -   Use Cloud Run for deploying the Flask API. Cloud Run automatically scales the application and abstracts away infrastructure management.

5.  **Google Cloud SQL or Google Big Query**:

    -   Use Cloud SQL with PostgreSQL for the relational database storage. Cloud SQL provides a fully managed database service.
    -   Use BigQuery for large-scale data analytics. It's a serverless, highly scalable data warehouse designed for business agility.

