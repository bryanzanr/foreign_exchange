# Foreign Currency

## Back-End (BE)
## Web Interview Test

## How the Applications Work

The web-application is based on Django Python Framework. It's implemented through Representational State Transfer Application Program Interface (REST-API). The assumptions that has been made are as follows::

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
* Create myapp/models.py for database migration.
* Create myapp/serializers.py for models instance.
* Create myapp/views.py for accessing the models.
* Create myapp/urls.py for routing the views.
* Create templates/ for HTML Custom Page.
* Create myapp/tests.py for unit-testing.

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

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used in backend development language (Python)
* [PostgreSQL](https://www.postgresql.org/) - Used to generate database

## Authors

* **Bryanza Novirahman** - *Fresh Graduate's from Computer Science University of Indonesia* - [LinkedIn](https://www.linkedin.com/in/bryanza-novirahman-902a94131)

## Important links
* [Docker](https://www.docker.com)
