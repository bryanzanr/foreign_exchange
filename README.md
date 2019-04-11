# Foreign Currency

## Back-End (BE)
## Web Interview Test

## How the Applications Work

The web-application is based on Django Python Framework. It's implemented through Django Representational State Transfer Application Program Interface (REST-API) and some others custom views on Hyper Text Markup Language (HTML). The assumptions that has been made are as follows::

![Database design](https://ibb.co/Q96xZc3)

1. Currency format is in ISO where has maximum character's length of 3.
2. Most of the variable is styled in snake case.
3. Date format in yyyy-mm-dd.
4. The last 7 day exchange is calculated for each currency.
5. The most recent 7 data points is calculated from the current date.
6. The average is calculated by sum up every data divided with their amount.
7. Some of the user interface (UI) are default and some others are custom.  

More detailed information can be found [here](https://drive.google.com/open?id=11kunl81ebg8U8jWqWiJw24ZLGRfSjfLh).

Design Decision:
* Create Dockerfile.
* Create docker-compose.yml
* Create Django project.
* Create Django app 'myapp'.
* Create myapp/models.py for database migration.
* Create myapp/serializers.py for models instance.
* Create myapp/views.py for accessing the models.
* Create myapp/urls.py for routing the views.
* Create myapp/templates/ for HTML Custom Page.
* Create myapp/tests.py for unit-testing.
* Refactor using myapp/forms.py for better validation.
* Refactor myapp/migrations for better variable's name.
* Create README.md
* Refactor better variable name and Finishing.  

## Getting Started (How to Run the Program)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites (How to set up your machine)

1. Navigate to the directory where you've cloned this repo and setting up the docker first.
2. Still in the directory where you've cloned this repo, install all its dependencies and run the app.

    ```bash
    docker-compose up
    ```

    Dependencies are all listed in `Dockerfile` and `docker-compose.yml`.

3. The app is now running! To check that the web is actually running,
try to send a GET request to it, for instance:

    ```bash
    curl http://127.0.0.1:8000/api/status
    ```

    or open `http://localhost:8000/api/status` from your browser. You should get a Javascript Object Notation (JSON) response that says:

    ```bash
    {list:[]}
    ```

### Installing (How to check and test the program)

1. Make sure you already pull the docker images and run the container.
Both are listed in `Dockerfile` and `docker-compose.yml` so if you followed the instructions to setup your machine above then they should already be installed and running.
2. You can run the check for running container ID with `docker ps` and for the installed images with `docker images` respectively.
3. To run the Postgre Structured Query Language (PosgreSQL) console in one command, you can use `docker exec -it <database container ID> psql -U postgres `. This is useful to check the database directly.
4. To run the tests, you can use `docker exec -it <web container ID> python manage.py test`.
5. For more info on what you can do with `docker`, run `docker --help`.

## Documentation

### Default Django

* [Current Currency](#current-currency)
* [Current Exchange](#current-exchange)

### Custom Django Views

* [Create Currency](#create-currency)
* [Create Exchange](#create-exchange)

### Functional API List

* [Get Average](#get-average)
* [Get Variance](#get-variance)
* [Delete Currency](#delete-currency)


## Current Currency
URL: GET - `http://localhost:8000/api/currency`

Example Response Body:

```json
[{
    "url": "http://localhost:8000/api/currency/1",
    "currency_from": "USD",
    "currency_to": "GBP"
}]
```

## Current Exchange
URL: GET - `http://localhost:8000/api/exchange`

Example Response Body:

```json
[{
    "url": "http://localhost:8000/api/exchange/1",
    "exchange_date": "2018-07-01",
    "exchange_rate": 0.75709,
    "currency": "http://localhost:8000/api/currency/1"    
}]
```


## Create Currency
URL: POST - `http://localhost:8000/api/add/`

Example Request Body:

```json
{
    "currency_from": "USD",
    "currency_to": "GBP"
}
```

Example Response Body:

```json
{
    "status": "True",
    "message": "Currency Inserted"
}
```

## Create Exchange
URL: POST - `http://localhost:8000/api/create/`

Example Request Body:

```json
{
    "exchange_date": "2018-07-01",
    "currency_from": "USD",
    "currency_to": "GBP",
    "exchange_rate": 0.75709
}
```

Example Response Body:

```json
{
    "status": "True",
    "message": "Exchange Inserted"
}
```

## Get Average
URL: POST - `http://localhost:8000/api/list/`

Example Request Body:

```json
{
    "exchange_date": "2018-07-01"
}
```

Example Response Body:

```json
{
    "status": "True",
    "exchanges": [{
      "currency_from": "USD",
      "currency_to": "GBP",
      "avg": 0.759366,
      "exchange_rate": 0.7609
      }]
}
```

## Get Variance
URL: POST - `http://localhost:8000/api/current/`

Example Request Body:

```json
{
    "currency_from": "USD",
    "currency_to": "GBP"
}
```

Example Response Body:

```json
{
    "status": "True",
    "exchange": {"average": 1.316904,
    "variance": 0.312},
    "exchanges": [{
      "exchange_date": "2019-04-08",
      "exchange_rate": 1.417
      }],
    "currency_from": "USD",
    "currency_to": "GBP"
}
```


## Delete Currency
URL: POST - `http://localhost:8000/api/untrack/`

Example Request Body:

```json
{
    "currency_from": "USD",
    "currency_to": "GBP"
}
```

Example Response Body:

```json
{
    "status": "True",
    "message": "Currency Deleted"
}
```

Postman's API Documentation can be found [here](https://documenter.getpostman.com/view/1319523/S1EMX18J).

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used in backend development language (Python)
* [PostgreSQL](https://www.postgresql.org/) - Used to generate database

## Authors

* **Bryanza Novirahman** - *Fresh Graduate's from Computer Science University of Indonesia* - [LinkedIn](https://www.linkedin.com/in/bryanza-novirahman-902a94131)

## Important links
* [Docker](https://www.docker.com)
