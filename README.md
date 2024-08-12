# drf-airport-service

API service for airport managing

# Installing using GitHub 

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
set SECRET_KEY=  

python manage.py migrate  
python manage.py runserver  


# Run with docker  

docker compose build  
docker compose up  

# Getting access 

create user via /api/user/register/    
get tokens via /api/user/token/
