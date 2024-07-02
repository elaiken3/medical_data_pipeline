## Problem

Preston Ventures has built out a process that digitizes medical records and extracts various targeted fields. We use this data to build out data products and analytics. A synthetic sample of this data is included in this local directory:

- *lifestyle.csv*
- *rx.csv*
- *conditions.csv*
- *labs.csv*
- *tests.csv*

This medical record data has been parsed based on the type, into the separate tables above. The data in these tables are raw, parsed directly from XML. There might be duplicates, typos, missing fields, etc.

We want to create a clean database from these different tables that we want to use as input into machine learning models.

### Dataset Overview

Each record is a specific event or “feature” for a person, with multiple potentially happening on the same day. Each table except RX has “feature” and “value” columns. The value of the “value”  column corresponds to the “feature” column. For example:

| feature | value | report_date |
| --- | --- | --- |
| Appearance | Walker | 1/1/2012 |

This means that the Appearance feature was tracked on 1/1/2012, and the value for Appearance that day was “walker”.

For each specific table there could be other columns that only apply to that specific category, for example RxNorm in RX, or ICDCode in conditions.

### Your Task:

1. Build a pipeline for each table that cleans the data from each table and outputs the table(s) for loading into SQL. Please include as much information from the raw data as possible. If removing data points or columns, provide an explanation.
    
    Bonus points: use OOP for pipeline design.
    
2. Design a schema for the resulting database for the clean data in SQL (your final clean tables from step 1 should match these).
    
    Create table statements (DDL) and a schema diagram are required.
    
    Set up, load the data, and tear down a SQL database for the project as part of the pipeline process.
    
3. Create the following transformations to be used as features for machine learning models or analytics:
    1. In Rx, whether a patient is taking alpha blockers medication - *boolean*
    2. The most recent HgB result for a patient - *number*
    3. Number of unique encounters in the last 6 months of the patient’s most recent date, across all data - *number*
    
    Bonus points: create 2 other features that you think might be useful for modeling a person’s health status
    
4. Create an API using Flask with different endpoints that would:
    1. Given a person_id, return all resources for that person in json format. Example response payload below
        
        ```json
        {
          "person_id": 123,
          "data": {
        		"lifestyle": [
        			...
        		],
        		"rx": [
        			...
        		],
        		...
          }
        }
        ```
        
    2. Given a person_id, return all calculated transformations from step 3
        
        ```json
        {
        	"person_id": 123,
        	"data": {
        		"gender_f": true,
        		"feature_x": 456,
        		...
        	}
        }
        ```
        
    
    We should be able to run the API locally and test it.
    
5. Discussion point #1: we receive this data from different data vendors. The vendors generate the data in a json file for each person at the time the record is created or updated in the source system. We have 1 million persons in our database and we estimate 10,000 of them to have updated records per day. How do you suggest we should
    1. Receive the data from the vendors?
    2. Ingest the data into our database?
    3. Minimize table locking during data ingestion?
    4. What do you think would be the best database for this data?
6. Discussion point #2: we would like to deploy this service to a cloud environment. What cloud provider and services would you use to deploy this solution?

You may build out the logic in whatever structure you wish, however it must use Python as the scripting language. The flavor of SQL you use is not important, just specify which flavor you are using.

In your submission, provide a markdown file with a description of your process for each of the steps above, as well as instructions and an example of how to use the entire pipeline.

When complete, zip your project up without the data and email it to:

ktehseen@prestonv.com

smourad@prestonv.com

jdodd@prestonv.com