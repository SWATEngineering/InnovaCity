FROM python:3.11-bookworm

WORKDIR app

COPY ./* ./

RUN pip install confluent-kafka

CMD ["python3","main.py"]