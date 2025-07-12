FROM python:3.10

WORKDIR /

COPY ./requirements.txt . 

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
