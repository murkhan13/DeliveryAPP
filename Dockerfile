# pull official base image
FROM python:3.8.2-alpine

ENV PATH = "/scripts:${PATH}"
# set work directory
# WORKDIR /home/mozley/Desktop/Django/DeliveryAPP

# add requirements (to leverage Docker cache)
# ADD ./requirements.txt /home/mozley/Desktop/Django/DeliveryAPP/requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk add libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .tmp gcc  libc-dev  build-base linux-headers
    # && pip install Pillow
RUN pip install -U pip
RUN pip install --no-binary pillow pillow

# install psycopg2 dependencies
RUN apk update && apk add  make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev postgresql-dev  musl-dev

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip3 install --upgrade pip
# add app
# ADD . /home/mozley/Desktop/Django/DeliveryAPP

COPY ./requirements.txt /requirements.txt
COPY ./scripts /scripts
RUN pip3 install -r requirements.txt
RUN apk del .tmp
RUN mkdir -p app
COPY ./cronDeliveryAPI /app/
ADD . .
WORKDIR cronDeliveryAPI


ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]
ENTRYPOINT ["../scripts/entrypoint.sh"]


# copy entrypoint.sh
# COPY ./entrypoint.sh .

# copy project
# COPY . .

# run entrypoint.sh
# ENTRYPOINT ["/home/mozley/Desktop/Django/DeliveryAPP/entrypoint.sh"]