FROM python:3.11-bookworm

WORKDIR /app

COPY . .

RUN pip install confluent-kafka

RUN ls

CMD ["python3","main.py"]