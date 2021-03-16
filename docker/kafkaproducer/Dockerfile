FROM python:3.6

COPY docker/kafkaproducer/*.py /app/kafka-consumer-sns-sqs/

COPY tests/test_data.json /app/kafka-consumer-sns-sqs/tests/test_data.json

WORKDIR /app/kafka-consumer-sns-sqs/

RUN pip install pipenv 

RUN pipenv install kafka-python

CMD pipenv run python /app/kafka-consumer-sns-sqs/kafka_producer.py