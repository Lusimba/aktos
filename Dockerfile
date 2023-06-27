FROM --platform=linux/amd64 python:3.8

RUN mkdir /app
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .