FROM ubuntu

RUN apt-get update -y && \
    apt-get install -y python3.8 && \ 
    apt-get install -y python3-pip && \
    apt-get install -y  sqlite3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["flask"]

CMD ["run", "--host", "0.0.0.0"]