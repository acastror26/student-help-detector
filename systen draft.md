The goal of this model is to predict the final grade in a class for a student given a number of indicators, in order to detect if the student needs extra help in the course.

The context of use for this model would be in an academic institution most likely a school or a higher education institution.

Requirements:
* Model must be readily available to use.
* App must be able to accept data on batch.
* App is allowed to store the data for retraining as long as there is no student identifiable information stored in database.
* Everyone is allowed to use the model for predictions but only the data from authenticated users is allowed to be stored.
* If the model stops being accurate there should be alerts for the ML engineer to refine it.
* If the app has a problem, the logs should save information about the issue.
* The system will receive feedback to an endpoint when the actual grades are uploaded at the end of the semester.
* Immediate processing is prefered but not a blocker.

Limitations:
* Limited budget -> stream deployment is out of question. On line is inefficient and more expensive. Apart from finantial reasons, the full data with the final result is given at the end of the month, so Batch should be used.
* Data might be riddled with human error -> must clean the dataset 
* Running on servers on site instead of the cloud


## System (simple version)
1. data which includes final grade is given via a csv at the end of the semester.
2. On adding new files to the csv folder:
- Clean the data
- Calculate drift
3. If drift detected,
- Log
- retrain
- Log results
4. New model is used for next predictions

Model will be made available via an application (if there's time to do this)


## Application side flows
### User uploads csv
#### Without final grades
1. User uploads csv to app
2. Application removes identifiable information except user id which is assumed to be the same on any campus system.
3. Application stores the data in db for the current semester.
4. Log
5. Return 200

#### With final grades
(same as previous)

### User pulls the most recent prediction report
#### Report available
1. User makes a get request to the endpoint
2. Application pulls the prediction from the right table
3. Application returns a csv (simplified flow) with the predictions
#### Report unavailable
1. User makes a get request to the endoint
2. Application tries to pulls the prediction
3. No prediction found/none ready
4. Return error message saying its not ready

## ML side flow
### Generate prediction report for ongoing period
1. Trigger (some period of time, like every two weeks)
2. Pull data from db
3. Get only data that has enough columns to predict (clean up and filter)
4. Run prediction model
5. Log
6. Store the result
### Final grades uploaded to db
1. Trigger (final grades available in db for the current semester, or auto trigger end of semester)
2. Detect drift
3. If drift, log alert
4. Grab historical data and retrain
5. Replace old model with the new one
6. Log results of retrain and that model got replaced


You are a python software engineer who follows best practices. Write a fastapi application that complies with the following criteria:
* It must be done as an hexagonal architecture with abstractions for each layer.
* The database must be handled with sqlalchemy and alembic.
* It must use dependency injector to handle dependencies. Dependencies here are the postgresql database and logstash.
* This is a dockerized app. Elastic search and kibana should also be running and their configuration must be added to the parent folder.
* All logs are handled by logstash.
* There is one table in database called `student-reports`. This table is defined with sqlalchemy. The columns are id, created_at, updated_at, user_id, start_date_period, end_date_period, gender, attendance_rate, study_hours_per_week, previous_grade, extracurricular_activities_count, parental_support, final_grade, prediction_final_grade, prediction_report_date. All fields are required except final_grade, prediction_final_grade and prediction_report_date.
* There is one endpoint called `update-csv`. This endpoint needs `start_date_period` and `end_date_period`in the body, and will receive a csv file. The csv and the body of this request is handled and data is stored in the database. The user gets 200 response if it was processed correctly. This csv will be used to search in db and update the row in db or insert it if needed. The structure for this table.
* There is another endpoint called `get-report`. This endpoint receives two query parameters `start_date_period` and `end_date_period` which it will use to query the student-reports table. It will also filter out rows that dont have a prediction_final_grade or that have final_grade. If no rows match, then return an error message saying that the report for the given period is not ready. If there is at least one row in the result, then return a downloadable csv file.
* This project must include terraform files and also github workflows to deploy. In this case for now the workflows are self hosted.
* Include a README that says how to run the project locally.