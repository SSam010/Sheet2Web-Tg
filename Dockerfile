FROM python:3.11.2
WORKDIR /usr/src/orders_website
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
