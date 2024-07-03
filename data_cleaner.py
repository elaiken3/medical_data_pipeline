import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection parameters
DB_NAME = "medical_records"
DB_USER = "postgres"
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = "5432"


class DataCleaner:
    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.data = pd.read_csv(filepath)
            logger.info(f"Loaded data from {filepath}")
        except Exception as e:
            logger.error(f"Error loading data from {filepath}: {e}")
            raise

    def remove_duplicates(self):
        original_len = len(self.data)
        self.data = self.data.drop_duplicates()
        new_len = len(self.data)
        logger.debug(f"Removed {original_len - new_len} duplicates from {self.filepath}")

    def handle_missing_values(self):
        # Flag missing values
        for column in self.data.columns:
            if self.data[column].isnull().sum() > 0:
                self.data[f'{column}_missing'] = self.data[column].isnull().astype(int)

    def standardize_dates(self, date_column):
        self.data[date_column] = pd.to_datetime(self.data[date_column], errors='coerce')
        invalid_dates = self.data[date_column].isnull().sum()
        logger.debug(f"Standardized dates in {date_column} for {self.filepath}, invalid dates: {invalid_dates}")

    def clean(self):
        logger.info(f"Starting cleaning process for {self.filepath}")
        self.remove_duplicates()
        self.handle_missing_values()

class LifestyleCleaner(DataCleaner):
    def clean(self):
        super().clean()
        self.standardize_dates('report_date')
    
    def feature_engineer(self):
        # Example: Add additional feature engineering logic specific to lifestyle data here
        pass

# Feature Engineering Functions
def is_taking_alpha_blockers(rx_data):
    alpha_blockers = ["FLOMAX"]
    return rx_data['rx_name'].isin(alpha_blockers).any()

def get_most_recent_hgb(labs_data):
    hgb_data = labs_data[labs_data['feature'] == 'Hemoglobin (HGB)']
    if not hgb_data.empty:
        return hgb_data.sort_values(by='feature_date', ascending=False).iloc[0]['value']
    return np.nan

def get_unique_encounters(person_data, person_id):
    recent_date = person_data['report_date'].max()
    six_months_ago = recent_date - pd.DateOffset(months=6)
    return person_data[person_data['report_date'] > six_months_ago]['report_date'].nunique()

def get_average_blood_pressure(tests_data):
    bp_data = tests_data[tests_data['feature'] == 'Blood pressure']
    if not bp_data.empty:
        bp_values = bp_data['value'].str.split('/', expand=True).astype(float)
        avg_systolic = bp_values[0].mean()
        avg_diastolic = bp_values[1].mean()
        return avg_systolic, avg_diastolic
    return np.nan, np.nan

def get_high_cholesterol_events(labs_data):
    cholesterol_data = labs_data[labs_data['feature'] == 'LDL']
    return (cholesterol_data['value'] > 130).sum()

def get_most_recent_a1c(labs_data):
    a1c_data = labs_data[labs_data['feature'] == 'A1c']
    if not a1c_data.empty:
        return a1c_data.sort_values(by='feature_date', ascending=False).iloc[0]['value']
    return np.nan



class RxCleaner(DataCleaner):
    def clean(self):
        super().clean()
        self.data['rx_norm'] = self.data['rx_norm'].astype(str).str.upper()
        self.standardize_dates('rx_date')

    def feature_engineer(self):
        self.data['taking_alpha_blockers'] = is_taking_alpha_blockers(self.data)

class ConditionsCleaner(DataCleaner):
    def clean(self):
        super().clean()
        self.standardize_dates('report_date')
    
    def feature_engineer(self):
        # Example: Add additional feature engineering logic specific to conditions data here
        pass

class LabsCleaner(DataCleaner):
    def clean(self):
        super().clean()
        self.standardize_dates('feature_date')
    
    def feature_engineer(self):
        self.data['value'] = pd.to_numeric(self.data['value'], errors='coerce')
        self.data['most_recent_hgb'] = get_most_recent_hgb(self.data)
        self.data['most_recent_a1c'] = get_most_recent_a1c(self.data)
        self.data['high_cholesterol_events'] = get_high_cholesterol_events(self.data)

class TestsCleaner(DataCleaner):
    def clean(self):
        super().clean()
        self.standardize_dates('report_date')
    
    def feature_engineer(self):
        avg_systolic_bp, avg_diastolic_bp = get_average_blood_pressure(self.data)
        self.data['average_systolic_bp'] = avg_systolic_bp
        self.data['average_diastolic_bp'] = avg_diastolic_bp

def execute_bash_script(action):
    try:
        result = subprocess.run(['bash', 'manage_db.sh', action, DB_PASS], capture_output=True, text=True)
        logger.info(result.stdout)
        if result.returncode != 0:
            logger.error(result.stderr)
            raise Exception(f"Error in {action} database")
    except Exception as e:
        logger.error(f"Failed to execute bash script for '{action}': {e}")
        raise

def load_data(df, table_name, engine):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"Loaded data into table {table_name}")
    except Exception as e:
        logger.error(f"Error loading data into table {table_name}: {e}")
        raise

def main():
    try:
        # Initialize and clean each CSV
        lifestyle_cleaner = LifestyleCleaner('lifestyle_ae.csv')
        lifestyle_cleaner.clean()
        lifestyle_cleaner.feature_engineer()
        lifestyle_cleaned_data = lifestyle_cleaner.data
        print(lifestyle_cleaned_data.columns)

        rx_cleaner = RxCleaner('rx_ae.csv')
        rx_cleaner.clean()
        rx_cleaner.feature_engineer()
        rx_cleaned_data = rx_cleaner.data
        print(rx_cleaned_data.columns)

        conditions_cleaner = ConditionsCleaner('conditions_ae.csv')
        conditions_cleaner.clean()
        conditions_cleaner.feature_engineer()
        conditions_cleaned_data = conditions_cleaner.data
        print(conditions_cleaned_data.columns)

        labs_cleaner = LabsCleaner('labs_ae.csv')
        labs_cleaner.clean()
        labs_cleaner.feature_engineer()
        labs_cleaned_data = labs_cleaner.data
        print(labs_cleaned_data.columns)

        tests_cleaner = TestsCleaner('tests_ae.csv')
        tests_cleaner.clean()
        tests_cleaner.feature_engineer()
        tests_cleaned_data = tests_cleaner.data
        print(tests_cleaned_data.columns)

        # Database connection parameters
        
        # Execute database setup
        execute_bash_script('setup')

        # Create a connection to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        # Load the cleaned data into the respective tables
        load_data(lifestyle_cleaned_data, 'lifestyle', engine)
        load_data(rx_cleaned_data, 'rx', engine)
        load_data(conditions_cleaned_data, 'conditions', engine)
        load_data(labs_cleaned_data, 'labs', engine)
        load_data(tests_cleaned_data, 'tests', engine)

        # Close the connection
        conn.close()

        # Execute database teardown
        # execute_bash_script('teardown')

    except Exception as e:
        logger.critical(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
