# Dockerfile

# pull the official docker image
FROM python:3.12

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

CMD [ "uvicorn", "app.main:app",  "--host", "0.0.0.0" ]