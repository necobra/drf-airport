# drf-airport-service

An API service for managing airport operations, built with Django Rest Framework (DRF).

# Installing using GitHub 

```bash
git clone https://github.com/necobra/drf-airport

python -m venv venv  
source venv/bin/activate  

pip install -r requirements.txt  

set POSTGRES_PASSWORD=<your_password>
set POSTGRES_USER=<your_user>
set POSTGRES_DB=<your_db>
set POSTGRES_HOST=<your_host>
set POSTGRES_PORT=5432
set PGDATA=/var/lib/postgresql/data
set SECRET_KEY=<your_secret_key>
set REDIS_LOCATION=redis://redis:6379/1

python manage.py migrate  
python manage.py runserver  
```

# Run with docker  

```bash
docker compose build  
docker compose up  
```

# Accessing the API

## Documantion
GET /api/schema/redoc/
## Swagger ui
GET /api/schema/swagger-ui/

## Create a User
### Register a new user via the registration endpoint:
POST /api/user/register/    

## Obtain Authentication Tokens
### After registration, obtain your tokens using:
POST /api/user/token/
