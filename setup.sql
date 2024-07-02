CREATE TABLE lifestyle (
        id SERIAL PRIMARY KEY,
        person_id INT,
        feature VARCHAR(255),
        value VARCHAR(255),
        report_date DATE
    );
    CREATE TABLE rx (
        id SERIAL PRIMARY KEY,
        person_id INT,
        feature VARCHAR(255),
        value VARCHAR(255),
        report_date DATE,
        rx_norm VARCHAR(255)
    );
    CREATE TABLE conditions (
        id SERIAL PRIMARY KEY,
        person_id INT,
        feature VARCHAR(255),
        value VARCHAR(255),
        report_date DATE,
        icd_code VARCHAR(255)
    );
    CREATE TABLE labs (
        id SERIAL PRIMARY KEY,
        person_id INT,
        feature VARCHAR(255),
        value VARCHAR(255),
        report_date DATE,
        loinc VARCHAR(255)
    );
    CREATE TABLE tests (
        id SERIAL PRIMARY KEY,
        person_id INT,
        feature VARCHAR(255),
        value VARCHAR(255),
        report_date DATE
    );