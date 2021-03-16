FROM python:3.6

COPY kafka_consumer /app/kafka-consumer-sns-sqs/kafka_consumer/

COPY docker/kafkaconsumer/kafka_consumer.py /app/kafka-consumer-sns-sqs/

COPY docker/kafkaconsumer/*.sh /app/kafka-consumer-sns-sqs/

COPY *.py /app/kafka-consumer-sns-sqs/

COPY Pip* /app/kafka-consumer-sns-sqs/

WORKDIR /app/kafka-consumer-sns-sqs/

RUN pip install pipenv 

RUN pipenv lock --requirements > requirements.txt

RUN pipenv install --dev

CMD ["sh", "-c", "/app/kafka-consumer-sns-sqs/run.sh && pipenv run python /app/kafka-consumer-sns-sqs/kafka_consumer.py"]
