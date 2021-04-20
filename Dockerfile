FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY config/requirements/requirements.txt /usr/src/app/

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
   && tar -xzf ta-lib-0.4.0-src.tar.gz \
   && cd ta-lib/ \
   && ./configure  --prefix=/usr \
   && make && make check && make install

WORKDIR /usr/src/app
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade pip

