FROM python:3.11-alpine

WORKDIR app

COPY ./* ./

RUN pip install confluent-kafka

CMD ["python3","main.py"]