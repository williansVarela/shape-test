FROM python:3.9.7-buster

# Setup all python related enviroment
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get install -y python python-dev postgresql-client

# Set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container
ADD . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN apt-get -y update && apt-get -y autoremove

CMD ["./start.sh"]
