FROM python:3.10

WORKDIR /

COPY ./requirements.txt . 

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN chmod +x /wait-for-it.sh

EXPOSE 8000

CMD ["sh", "-c", "/wait-for-it.sh postgres:5432 -- uvicorn app.main:app --host 0.0.0.0 --port 8000"]
