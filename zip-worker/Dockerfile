# Build upon this image "alpine" is a lightweight distro
FROM python:3.7-alpine

# Copy requirements.txt
#COPY ./requirements.txt /app/requirements.txt

# Install all the requirements
#RUN pip install -r /app/requirements.txt

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app



RUN mkdir -p /app/out
VOLUME /app/out
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# How to run it when we start up the box?
CMD ["./zip_worker.py"]