ARG TARGET_ARCH
FROM ${TARGET_ARCH}python:3.8 as build
WORKDIR /app

ADD requirements .
RUN pip install -r requirements
ADD . .

FROM build as map-api
EXPOSE 8080
CMD ["python", "app.py"]
