""" Copyright 2020 Expedia, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

import json
import os
from kafka import KafkaProducer
from kafka import KafkaConsumer
import time
from kafka.errors import NoBrokersAvailable
import logging

logging.basicConfig(level="DEBUG")
LOG = logging.getLogger(__name__)


def main():

    with open("tests/test_data.json") as fp:
        test_event = json.load(fp)
    event_count = os.environ.get("EVENT_COUNT")

    retry = 0; kafka_available = False
    while(not kafka_available and retry <= 15):
        try:
            # To determine if kafka server is ready and topic is created
            consumer = KafkaConsumer(os.environ.get("KAFKA_TOPIC"), bootstrap_servers=os.environ.get("PRODUCER_BOOTSTRAP_SERVERS"))
            kafka_available = True

            producer = KafkaProducer(bootstrap_servers=os.environ.get("PRODUCER_BOOTSTRAP_SERVERS"),
                                    value_serializer=lambda x: json.dumps(x).encode("utf-8"))
            LOG.debug(f"Kafka producer: Retry count: {retry}")
            count = 0; c = True
            while(c):
                LOG.debug(f"test_event: {test_event}")
                producer.send(os.environ.get("KAFKA_TOPIC"), value=test_event)
                count = count + 1
                if event_count:
                    if count >= int(event_count):
                        LOG.debug(f"Event count={event_count}")
                        c = False
        except NoBrokersAvailable:
            LOG.warning("Kafka server is not yet available")
            retry = retry + 1
            time.sleep(5)
        except(ConnectionResetError, ConnectionError):
            LOG.warning("Kafka topic is not yet available")
            retry = retry + 1
            time.sleep(5)
        except Exception as e:
            LOG.error(e)
            retry = retry + 1
            time.sleep(5)



if __name__ == "__main__":
    main()
