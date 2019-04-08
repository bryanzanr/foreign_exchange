# Foreign Currency

## Back-End (BE)
## Web Interview Test

## How the Applications Work

The web-application is based on Django Python Framework. It's implemented through Representational State Transfer Application Program Interface (REST-API). The assumptions that has been made are as follows::

![Database design](https://ibb.co/Q96xZc3)

1. Currency format is in ISO where has maximum character's length of 3.

More detailed information can be found [here](https://drive.google.com/open?id=11kunl81ebg8U8jWqWiJw24ZLGRfSjfLh).

Design Decision:
* Create myapp/models.py for database migration.

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
    curl http://127.0.0.1:8000/list
    ```

    or open `http://localhost:8000/list` from your browser. You should get a
    Javascript Object Notation (JSON) response that says:

    ```bash
    {list:[]}
    ```

### Installing (How to run the tests/linters)

1. Make sure you already pull the docker images and run the container.
Both are listed in `Dockerfile` and `docker-compose.yml` so if you followed the instructions to setup your machine above then they should already be installed and running.
2. You can run the check for running container ID with `docker ps` and for the installed images with `docker images` respectively.
3. To run the Postgre Structured Query Language (PosgreSQL) console in one command, you can use `docker exec -it <database container ID> psql -U postgres `. This is useful to check the database directly.
4. For more info on what you can do with `docker`, run `docker --help`.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used in backend development language (Python)
* [PostgreSQL](https://www.postgresql.org/) - Used to generate database

## Authors

* **Bryanza Novirahman** - *Fresh Graduate's from Computer Science University of Indonesia* - [LinkedIn](https://www.linkedin.com/in/bryanza-novirahman-902a94131)

## Important links
* [Docker](https://www.docker.com)
