FROM ubuntu:14.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    git \
        python \
        python-pip \
        python-dev \
    python-scipy \
    python-numpy \
        build-essential \
        pkg-config \
        libsqlite3-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        libssl-dev \
        python-joblib

RUN pip install -U pip

WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -U -r requirements.txt

ADD . /app

# RUN pip install .

EXPOSE 8889

CMD [ \
    "/usr/bin/python", \
    "-m",  "classifiers" \
]
