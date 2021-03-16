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
import logging
import traceback
import boto3

from kafka import KafkaConsumer
from kafka_consumer.messaging import Messaging
from kafka_consumer.configs.kafka import KAFKA_TOPIC, BOOTSTRAP_SERVERS, AUTO_OFFSET_RESET, CONSUMER_TIMEOUT_MS
from kafka_consumer.configs.log import LOG_LEVEL
from kafka_consumer.configs.consumers.aws import AWS_ENDPOINT_URL

logging.basicConfig(level=LOG_LEVEL if LOG_LEVEL else "INFO")
LOG = logging.getLogger(__name__)


class KafkaProcessor:
    """
    KafkaProcessor reads data from a given KAFKA topic, applies transformations if any and sends transformed data to a
    given AWS SNS/SQS. Assumes the resource using this has adequate permissions to read data from kafka topic.
        transformer: Optional. Custom transformation function that can be applied prior to sending event to AWS SNS/SQS
        transform_type: Optional. Used in conjunction with the transformer function to have variations of transformations
                        within the same transformer.
        consumer_type: Required. Type of AWS consumer. Expected value is "sns" or "sqs"
    """
    def __init__(self, transformer=None, transform_type=None, consumer_type="sns"):
        super().__init__()
        LOG.debug(f"bootstrap_servers, {BOOTSTRAP_SERVERS}")
        if CONSUMER_TIMEOUT_MS:
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                auto_offset_reset=AUTO_OFFSET_RESET if AUTO_OFFSET_RESET else "latest",
                enable_auto_commit=False,
                consumer_timeout_ms=int(CONSUMER_TIMEOUT_MS)
            )
        else:
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                auto_offset_reset=AUTO_OFFSET_RESET if AUTO_OFFSET_RESET else "latest",
                enable_auto_commit=False
            )
        self.transformer = transformer
        self.transform_type = transform_type
        self.consumer_type = consumer_type
        self.client = boto3.client(self.consumer_type, endpoint_url=AWS_ENDPOINT_URL)

    def process_message(self):
        LOG.debug("Processing messages")
        for record in self.consumer:
            try:
                data = json.loads(record.value)

                LOG.debug(f"Event received: {data}")
                if self.transformer:
                    transformedEvent = self.transformer(data)
                    LOG.debug(f"Transformed Event: {transformedEvent}")
                    if transformedEvent:
                        msg = Messaging(transformedEvent, self.consumer_type, self.client)
                        if not msg.send_event():
                            LOG.warning(f"Event couldnot be sent: {data}")
                else:
                    LOG.warning(f"No event transformations applied: {data}")
                    msg = Messaging(data, self.consumer_type, self.client)
                    if not msg.send_event():
                        LOG.warning(f"Event couldnot be sent: {data}")

            except Exception as e:
                LOG.error('Error reading Kafka data', str(e))
                LOG.error(traceback.format_exc())
                return False
        return True

