FROM nginx:alpine

RUN apk add --no-cache netcat-openbsd

COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/wait-for.sh", "fastapi", "8000", "nginx"]
