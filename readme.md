# Power balancer full stack app

## Stack 
- fronted: Angular 21
- backend: Fastapi
- database: Postgres 16

## Project description
Simple full stack power balancer to display and control energy consumption based on maximum source capacity. 

### Frontend
A fresh angular template was used for the frontend.  
- Routes 
- Feature based components with separate models and api service classes
- Components (all standalone)
- PrimeNG for components
- Tailwindcss for styling

PrimeNg with tailwind was used to make styling easier. Routes were setup for future expansion, despite currently only having a single route. 
Each section has its own domain setup (consumers and sources in the dashboard). Here the models and api connection is kept close to the actual domain models.


### Backend
Fastapi is used to create a REST api that connects the frontend to the DB. Sqlalchemy and alembic are widely adopted and work well together with fastapi as ORM and db schema migrations. 
Pydantic is used a schema checker for in/outgoing json data <-> python conversion to validate data.

For the selective deactivation of certain consumers a PATCH request was chosen. Deactivate/activate verbs dont match well with REST guidelines and a PATCH most closely resembles the nature of the action: A partial modification of an existing object. 
Additionally, a decativate-by-priority endpoint is created to make it easier to deactivate all consumers over a certain priority. For this a POST request was used as its modification but we're unsure which objects it affects (not in the request that is). 

Simple CRUD is omitted as no specification was given that any other data input besides loading the json files is useful or desired. It can be added fairly simply using the existing structure and pydantic schemas


### Data import
Three sql models were defined based on the given input

Source (all fields from data input)
- id            
- name
- capacity     

Consumer
- id (added for indexability)
- name (unique true, perhaps this was primary key before)
- priority

ConsumerPowerRequirement, extended many-to-many field, connecting a Source to a Consumer. 
- id 
- consumer_id
- source_id
- capacity 
- is_active (bool added here to allow flexible downsize/upsizing of power capacity, perhaps in the future a certain source 
is shut down or has maintenance -> allows deactivation of specific source_id AND consumer_id capacities)

The current dataset allows for composite keys of consumer_id and source_id, but no clear spec is given, so this could result in future conflicts -> simple id was chosen. For public exposure, the autoincremented id fields could be replaced by name slugs or uuids, however, for indexability a simple autoincremented key is preferred. A double key system would make sense if guessing ids results in security concerns. 



## Improvements
This project was build to demo a full-stack application. Main philosophy was to generate a project with: 
Simple startup flow for new users (preset docker) and be extensible for future work. 

- db is a simple postgres container with a small initialization script to set minimal permisisons, but not a production ready setup. 
- backend main.py has a lot of wildcards, not suitable for prod
- backend has no caching on any endpoint, for larger datasets with stale readlyonly data this can be improved
- backend/frontend has 0 auth, anyone can see everything
- frontend has simple datastore; dashboard.store.js for data state management. A more clean approach would be a full api store using ngrx for fetching data and keeping track of current state. 
- Data import now a simple for loop script that blocks the db during import. Because the amount of data to import is very limited its not a real issue right now. 
With increased data import load this blocks any db call while the script is running. A more advanced import script is required for real world use which would include: 
    - retry logic
    - error handling (duplicate objects, missing source ids)
    - batching (e.g. a spring-batch setup)

- docker-compose now includes all services, this is done to get the project up and running faster locally. Its better to plit into different cloud hosting steps. 
Especially, since now the frontend serves static files, but all traffic still flows through nginx, running the frontend on S3+cloudfront is cheaper and faster in almost all cases. 
- A dashboard.store.js is included for data state management. A more clean approach would be a full api store using ngrx for fetching data and keeping track of current state. 
- Enhanced ui component testing 
- Not all components fully use PrimeNg cmponents, can be made more aligned by updating these components
- Full ci/cid pipeline with auto build steps improves deployment



## Project contents 

| folder              | Purpose                                                                          |
|----                 | ---                                                                              |
| /database/          | Simple setup to get a local postgres database running                            | 
| /fastapi_backend/   | Api project folder that runs the api (connects to database)                      | 
| /angular_frontend/  | Angular project, also holds static build files serve oby dockers' Nginx instance  | 


### fastapi_backend
```
├── app
│   ├── api
│   │   └── routers and api endpoints 
│   ├── core   
│   │   └── app config/settings
│   ├── db
│   │   └── db connection files
│   ├── models
│   │   └── sql alchemy models
│   ├── schemas
│   │   └── pydantic DTO classes
│   ├── services
│   │   └── business logic
│   └── tests
│       └── pytest folder
├── main.py
├── data  (db seed data)
│   ├── consumers.json
│   └── sources.json
└── http
    └── simple http endpoint testers (REST client extension)
```

### angular_frontend
```
├── src
│   └── app
│       ├── dashboard
│       │   ├── dashboard.store.ts     (state store)
│       │   ├── barchartcomponent
│       │   │   └── bar chart visual component
│       │   ├── consumers
│       │   │   ├── consumers.api.ts       (api service)
│       │   │   ├── consumers.models.ts    (domain models)
│       │   │   └── consumers component
│       │   └── sources
│       │       ├── sources.api.ts         (api service)
│       │       ├── sources.models.ts      (domain models)
│       │       └── sources component
│       ├── app.routes.ts              (route definitions)
│       └── app.config.ts             (app configuration)
```



## Running the app locally

The easiest way to get the app running is to use the `docker-compose.yml` file to start all services.

#### 1. Create backend env file

Copy `fastapi_backend/.env.example` to `fastapi_backend/.env` and adjust passwords if needed.


#### 2. Run docker. 

```
docker compose up -d
```

This starts the database (postgres), fastapi app and an Nginx instance. 
The database starts with ```POSTGRES_ADMIN_USER``` and ```POSTGRES_ADMIN_PASSWORD``` and auto initializes a new user based on the environment variables in ```APP_DB_USER``` and ```APP_DB_PASSWORD```. The app user is then used by fastapi for all db operations. 

The database has no data, we need to run albembic migrations and import seed data.

#### 3. Create db schema and import data

Run commands in the docker container
```
docker exec -it fastapi_app /bin/sh
```

Create db schema
```
alembic upgrade head
```

import sources.json 
```
python sources_import.py
```

import consumers.json 
```
python consumers_import.py
```


Now the database should contain the seed data. The frontend should be live on localhost:4200, the backend on localhost:8100


## Running local dev servers

### Backend

#### Setup database
Only complete this step if the previous docker setup was skipped. If theres a running db with data, just use that (and perhaps turn off the fastapi and nginx containers)

Otherwise, run the docker-compose-dbonly.yml file to start only a database instance. 

```
docker compose -f fastapi_backend/docker-compose-dbonly.yml up -d
```

Then run schema and initialization scripts from step 3 of the docker setup.


#### Running fastapi

run the local fastapi setup from the fastapi folder ```cd fastapi_backend```


```
python -m venv .venv
```

Activate virtual environment:

Windows:

```
.venv\Scripts\Activate.ps1
```

macOS/Linux (bash/zsh):

```
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

```
uvicorn app.main:app --reload --port 8100
```
Port 8100 is required as the frontend assumes 8100 as local port. (can be altered, but 8100 was used to prevent conflicts with the default port 8000)


#### Running tests
Run all tests (end to end only possible with running db)
```
pytest 
```

To run specific test, pytest markers were added. (options: "e2e", "integration", "unit") e.g. 
```
pytest -m integration
```


### Frontend 
Inside the angular folder (``` cd angular_frontend``` )

Install dependencies
```
npm install
```

Open dev server
```
npm start
```

Notes:
- `npm start` uses Angular CLI (`ng serve`) from project dependencies
- If your browser does not open automatically, use `npm start -- --open`.


#### Recreate static files 
The base docker image uses static files served by nginx. To recreate these files after changing the frontend run: 
```
ng build --configuration production
```



