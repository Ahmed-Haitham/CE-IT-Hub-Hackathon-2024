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

ARG ADMIN_USERNAME
ENV ADMIN_USERNAME=${ADMIN_USERNAME}

ARG ADMIN_PASSWORD
ENV ADMIN_PASSWORD=${ADMIN_PASSWORD}

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]