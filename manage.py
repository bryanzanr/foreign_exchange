#!/usr/bin/env python
import os
import sys

# import code
# from os.path import join, dirname
import subprocess

import click
# from dotenv import load_dotenv
# import pytest

# def load_app():
#     # Environment variable MUST be set before importing the app
#     dotenv_path = join(dirname(__file__), '.env')
#     load_dotenv(dotenv_path)

#     from csuibot import app
#     return app


@click.group()
def manage():
    """Script to manage tasks outside the application itself."""
    pass


# @manage.command()
# def shell():
#     """Run a shell with custom context."""
#     context = dict(app=load_app())
#     try:
#         from IPython import embed
#     except ImportError:
#         code.interact(local=context)
#     else:
#         embed(user_ns=context)


@manage.command()
def runserver():
    """Run the application server."""
    # load_app().run()
    # manage()
    pass


@manage.command()
def migrate():
    """Synchronize Database."""
    pass


@manage.command()
def makemigrations():
    """Merge Database."""
    pass


@manage.command()
def help():
    """Show Default Command Only."""
    pass


@manage.command()
def collectstatic():
    """Show Default Command Only."""
    pass


@manage.command()
def test():
    pass
    """Run the tests."""
    # Environment variable MUST be set before importing the app
    # dotenv_path = join(dirname(__file__), 'tests', '.env')
    # load_dotenv(dotenv_path)

    # sys.exit(pytest.main([]))


# @manage.command()
# def lint():
#     """Run the linters."""
#     sys.exit(subprocess.call(['flake8']))


@manage.command()
def check():
    """Run linters and tests.

    Use this command to check before making a merge request."""
    # Environment variable MUST be set before importing the app
    # dotenv_path = join(dirname(__file__), 'tests', '.env')
    # load_dotenv(dotenv_path)

    # sys.exit(subprocess.call(['flake8']) or pytest.main([]))
    sys.exit(subprocess.call(['flake8']))


if __name__ == "__main__":
    # manage()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flyit.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    manage()
