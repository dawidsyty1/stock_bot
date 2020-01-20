## The architecture.

| Location             |  Content                                   |
|----------------------|--------------------------------------------|
| `/app`           | Django Project            |
| `/scraper   `       | The catalog contains a mechanism to scrape images/texts from websites.|
| `/config`     |  Files with uwsgi/redis/enviroment/requirements configuration  |


## Run from docker-compose, before starting the application, you have to set in config/env.secret variable.
    SECRET_KEY - required by Django.

```bash

    docker-compose build
    docker-compose up

```
##
## Load datas fixtures and start test.
```bash
    docker-compose exec web python3 manage.py migrate --database test
    docker-compose exec web python3 manage.py loaddata scraper/fixtures/*.json --database test
    docker-compose exec web python3 manage.py test
```
##
## Get Rest API service address IP.
```bash

    docker-compose exec service_name ip a

```
##



 
