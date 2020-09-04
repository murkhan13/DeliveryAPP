# pull official base image
FROM python:3.8.2-alpine
# set work directory
WORKDIR /home/mozley/Desktop/Django/DeliveryAPP

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /home/mozley/Desktop/Django/DeliveryAPP/requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk add libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
RUN pip install -U pip
RUN pip install --no-binary pillow pillow

# install psycopg2 dependencies
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev postgresql-dev gcc  musl-dev

# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip3 install --upgrade pip
# add app
ADD . /home/mozley/Desktop/Django/DeliveryAPP
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/home/mozley/Desktop/Django/DeliveryAPP/entrypoint.sh"]