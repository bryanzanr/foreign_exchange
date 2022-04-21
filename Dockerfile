# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /foreign_currency

# Set the working directory to /foreign_currency
WORKDIR /foreign_currency

# Copy the current directory contents into the container at /foreign_currency
ADD . /foreign_currency/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt