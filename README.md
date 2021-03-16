# Kafka Consumer for AWS SNS/SQS

Kafka Consumer Python Library. This library can be used to fetch events synchronously from a given kafka topic, transform the events if neccessary and send them to an AWS SNS/SQS. The library assumes that the resource using this library has permissions to receive events from kafka and send events to AWS SNS/SQS.

```sh
pip install git+https://github.com/ExpediaGroup/kafka-consumer-sns-sqs.git#egg=kafka-consumer-sns-sqs
```

# Usage

## Configuration

```sh
# Environment variables
DOCKER_REGISTRY=awesome.dockerregisty.com
IMAGE_TAG=unique-tag
KAFKA_TOPIC=kafka-topic
BOOTSTRAP_SERVERS=bootstrapservers
EVENT_TOPIC=sns-topic-arn
QUEUE_URL=sqs-queue-url

# optional
LOG_LEVEL=DEBUG  # default=INFO
AUTO_OFFSET_RESET=earliest # default=latest
CONSUMER_TIMEOUT_MS=5000 # Not set by default, if set will be used as a condition to stop consumer iteraton
```

# User Environment

## Setup

### Install `pipenv`

```sh
brew install pipenv
```

### Setup environment and install dependencies

```sh
pipenv install -e .
```

## Use

```python
from kafka_consumer.processor import KafkaProcessor

processor = KafkaProcessor(
    transformer=<custom optional transformer function>, 
    transform_type=<custom optional transform type>, 
    consumer_type=<"sns" or "sqs">
)

processor.process_message()
```

NOTE: If using a custom transformer function, design it to take in an input event from kafka, 
an optional transform_type to use the same function for different transformations and
return a JSON payload to be sent to AWS SNS/SQS.

# Development Environment

## Setup

### Install `pipenv`

```sh
brew install pipenv
```

### Setup environment and install dependencies

```sh 
make install
```

## Run tests

```sh
make test
```

## Enter the pipenv shell

(See https://realpython.com/pipenv-guide/ for more info.)

```sh
pipenv shell
```

## Build

```sh
make build
```

## Docker build

```sh
docker-compose build kafkaconsumer
```

## Docker run within AWS

```sh
docker run --env-file <env-file> kafkaconsumer
```

## Docker run outside AWS

```sh 
docker run -v /Users/$USER/.aws/:/root/.aws:ro --env-file <env-file> kafkaconsumer
```

# Local container stack setup end to end (KAFKA to AWS SNS)

## Initial Setup

### Configure the aws profile to use the following:

```sh
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
echo "[default]" > ~/.aws/config
echo "region = us-west-2" >> ~/.aws/config
echo "output = json" >> ~/.aws/config
```

### Create a docker network

```sh
docker network create -d bridge localstack-net
```

### Set the following environment variables:

DOCKER_GATEWAY_HOST can be found by inspecting the network 

```sh
docker network inspect localstack-net

DOCKER_GATEWAY_HOST=<docker gatway host>
```

To use kafka external to the docker such as your local machine

```sh
OUTSIDE_HOSTNAME=<your desired external hostname, defaulted to localhost>

KAFKA_TOPIC=<your desired kafka topic name>
EVENT_TOPIC=arn:aws:sns:us-west-2:000000000000:TEST_SNS_TOPIC
PRODUCER_BOOTSTRAP_SERVERS=${DOCKER_GATEWAY_HOST}:9092
BOOTSTRAP_SERVERS=${DOCKER_GATEWAY_HOST}:9092
AWS_ENDPOINT_URL=http://${DOCKER_GATEWAY_HOST}:4566
LOCAL_STACK=True
```

### Run the following command:

```sh 
docker-compose up
```

This sets up the following services:

- `awslocalstack` - aws local stack with SNS as edge service (`http://${DOCKER_GATEWAY_HOST}:4566`) and test SNS topic(`arn:aws:sns:us-west-2:000000000000:TEST_SNS_TOPIC`) created
- `zookeeper` - zookeeper service 
- `kafka` - Kafka Broker with a test kafka topic created, topic name is configurable with `${EVENT_TOPIC`}
- `kafkaproducer` - Kafka event Producer, event count is configurable with `${EVENT_COUNT}`, will be continuous flow of events if not provided
- `kafkaconsumer` - Kafka Consumer, fetches events from kafka and sends events to SNS (uses the current library)
