FROM python:3.8-slim as board-api
WORKDIR /app


ADD requirements .
RUN pip install -r requirements
ADD . .

ARG DB_HOST
ARG DB_PORT
ARG DB_PASS
ARG DB_USER
ARG DB_NAME

ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV DB_PASS=$DB_PASS
ENV DB_USER=$DB_USER
ENV DB_NAME=$DB_NAME

EXPOSE 8080
CMD ["python", "app.py"]
