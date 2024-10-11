# Student help detector

## Description

The goal of this project is to aid a company in determining which students might fail in a given course. For this purpose, the model backend will generate reports every three weeks until the end of the period, which the user can then download via app.

## Problem context

The company manages a business that sells upskilling solutions via online courses, and the efficacy of this business model gears on determining the value that students managed to obtain from the program. Enterprise clients in particular which pay for upskilling want to see that the beneficiaries of the program use the skills they learned after the course ends. 

After internal review, the company has determined that the more a student receives further help in the topics they're struggling in, the better the final grades are.

Therefore, the company wants to predict which students might require additional help from the instructors and teaching assistants.

### Requirements

#### Domain
* Initially, the model will work with just one client, which is a university. Indicators are expected to be related to this environment.

#### Application
* There must be an application that receives and processes csv with the data. These request could be made at any time and data in database must be updated accordingly for the student in the particular course.
* The application must have a way to download the most recent report for the current period.
* Authentication is not required for this POC.

#### Reports
* At least every two weeks and at most every four weeks, generate a report that predicts the final grades for a given period.

#### Feedback
* Final grades are uploaded in the form of a csv at the end of the course.

#### Storage
* Permission has been granted to store user data as long as there's no specific identifiable information such as email, name, etc. aside from the universal user_id which is always given in the csv.

### Limitations

1. This is mostly a POC so limited budget is expected.
2. Provided data for initial training is very specific to the current domain, and resulting model might not be effective elsewhere.
3. POC provided data for initial training is small.

## Data
Dataset was obtained from: https://www.kaggle.com/datasets/haseebindata/student-performance-predictions/data

Initial dataset included in [training data directory](/model/training_data/initial_training_data.csv).

## The solution

### Architecture


#### Training infrastructure
* PostgreSQL
* MLFlow
* Elastic

#### Github actions
* Includes testing, model training, and deployment.
* Pipelines are triggered by code changes and on schedule at times.

#### Serving Infrastructure
* ELK stack for monitoring.
* Includes an api that will accept csv to process and return reports if available.

#### User interaction
* API REST requests.


## Running this project
### Prerequisites

- Docker
- Docker Compose
- Terraform (for deployment)

### How to Run the Project Locally

Build and run the application:

```bash
docker-compose up --build
```
The application will be available at http://localhost:8000. Kibana will be available at http://localhost:5601.

### Apply migrations:

```bash
docker-compose exec fastapi alembic upgrade head
```
The database, Elasticsearch, and Logstash will be automatically configured.

### Terraform Deployment
```bash
cd terraform
terraform init
terraform apply
```