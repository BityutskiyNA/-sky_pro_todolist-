# pull official base image
FROM python:3.09-slim

# set work directory
WORKDIR /usr/src/todolist

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY todolist/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./todolist .

#ENTRYPOINT ["python", "manage.py", "migrate", "--noinput"]