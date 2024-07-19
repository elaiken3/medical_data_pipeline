-- Drop tables if they exist
DROP TABLE IF EXISTS lifestyle;
DROP TABLE IF EXISTS rx;
DROP TABLE IF EXISTS conditions;
DROP TABLE IF EXISTS labs;
DROP TABLE IF EXISTS tests;

-- Create the tables
CREATE TABLE lifestyle (
    impairment_category VARCHAR(255),
    impairment VARCHAR(255),
    lifestyle_category VARCHAR(255),
    feature_type VARCHAR(255),
    feature VARCHAR(255),
    report_date DATE,
    clinician_specialty VARCHAR(255),
    value VARCHAR(255),
    secondary_value VARCHAR(255),
    person_id INT,
    impairment_missing INT,
    value_missing INT,
    secondary_value_missing INT
);

CREATE TABLE rx (
    impairment_category VARCHAR(255),
    impairment VARCHAR(255),
    din VARCHAR(255),
    rx_name VARCHAR(255),
    rx_type VARCHAR(255),
    start_date DATE,
    end_date DATE,
    rx_date DATE,
    rx_norm VARCHAR(255),
    person_id INT,
    impairment_category_missing INT,
    impairment_missing INT,
    din_missing INT,
    rx_type_missing INT,
    end_date_missing INT,
    rx_norm_missing INT,
    taking_alpha_blockers BOOLEAN
);

CREATE TABLE conditions (
    id INT,
    impairment_category VARCHAR(255),
    impairment VARCHAR(255),
    feature_type VARCHAR(255),
    feature VARCHAR(255),
    icd_code VARCHAR(255),
    report_date DATE,
    clinician_specialty VARCHAR(255),
    value VARCHAR(255),
    person_id INT,
    impairment_category_missing INT,
    impairment_missing INT,
    icd_code_missing INT,
    value_missing INT
);

CREATE TABLE labs (
    impairment_category VARCHAR(255),
    impairment VARCHAR(255),
    feature_type VARCHAR(255),
    loinc VARCHAR(255),
    feature_date DATE,
    feature VARCHAR(255),
    value VARCHAR(255),
    normal_range_of_value VARCHAR(255),
    result_evaluation_or_flag VARCHAR(255),
    person_id INT,
    impairment_missing INT,
    normal_range_of_value_missing INT,
    result_evaluation_or_flag_missing INT,
    most_recent_hgb FLOAT,
    most_recent_a1c FLOAT,
    high_cholesterol_events INT
);

CREATE TABLE tests (
    impairment_category VARCHAR(255),
    impairment VARCHAR(255),
    feature_type VARCHAR(255),
    feature VARCHAR(255),
    icd_code VARCHAR(255),
    report_date DATE,
    value VARCHAR(255),
    person_id INT,
    impairment_category_missing INT,
    impairment_missing INT,
    icd_code_missing INT,
    value_missing INT,
    average_systolic_bp INT,
    average_diastolic_bp INT
);
