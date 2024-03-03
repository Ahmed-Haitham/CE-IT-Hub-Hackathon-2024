# Dockerfile

# pull the official docker image
FROM python:3.12

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project - running from app context
COPY . .

ARG JWT_SECRET_KEY
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}

ARG JWT_REFRESH_SECRET_KEY
ENV JWT_REFRESH_SECRET_KEY=${JWT_REFRESH_SECRET_KEY}


CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]