# Build upon this image "alpine" is a lightweight distro
FROM python:3.7-alpine

# Copy requirements.txt
#COPY ./requirements.txt /app/requirements.txt

# Install all the requirements
#RUN pip install -r /app/requirements.txt

# Copy everthing from . to /app inside the 'box'

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN mkdir -p /app/out

VOLUME /app/out

WORKDIR /app

ADD . .
# How to run it when we start up the box?
CMD ["./worker.py"]