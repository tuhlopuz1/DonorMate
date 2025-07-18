FROM python:3.10

WORKDIR /

COPY ./requirements.txt . 

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN chmod +x /wait-for-it.sh

CMD ["sh", "-c", "/wait-for-it.sh rabbitmq:5672 -- /usr/local/bin/python bot.py"]
