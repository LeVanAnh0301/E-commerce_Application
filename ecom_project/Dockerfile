FROM python:3.12.0

# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip3 install pipenv && pipenv install --system && pip3 install -r requirements.txt

# Copy project
COPY .env /code/
COPY . /code/

