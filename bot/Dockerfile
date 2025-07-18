FROM python:3.10

WORKDIR /

COPY ./requirements.txt . 

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./wait-for-it.sh /wait-for-it.sh

RUN chmod +x /wait-for-it.sh

COPY . .

CMD ["python", "bot.py"]
