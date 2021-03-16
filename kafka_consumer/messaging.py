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

import logging
import traceback
import json
from kafka_consumer.configs.consumers.aws import EVENT_TOPIC, QUEUE_URL
from kafka_consumer.configs.log import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL if LOG_LEVEL else "INFO")
LOG = logging.getLogger(__name__)


class Messaging:
    """
    Messaging is used to send data to a given AWS SNS/SQS. Assumes the resource using it has adequate
    permissions to send data to AWS SNS/SQS.
        message: Required. Message to be sent to AWS SNS/SQS
        consumer_type: Required. Type of AWS consumer. Expected value is "sns" or "sqs"
        client: Required. SNS/SQS client
    """
    def __init__(self, message, consumer_type, client):
        super().__init__()
        self.message = message
        self.topic = EVENT_TOPIC
        self.queueurl = QUEUE_URL
        self.consumer_type = consumer_type
        self.client = client

    def send_event(self, attributes=None):
        if self.consumer_type == "sns":
            return self.send_to_sns(attributes)
        if self.consumer_type == "sqs":
            return self.send_to_sqs(attributes)
        else:
            return False

    def send_to_sns(self, attributes=None):
        try:
            messageAttributes = {}
            if attributes:
                for attribute in attributes:
                    messageAttributes[attribute] = {
                        'DataType': 'String.Array',
                        'StringValue': json.dumps(attributes[attribute])
                    }

            response = self.client.publish(
                TopicArn=self.topic,
                Message=json.dumps(self.message),
                MessageAttributes=messageAttributes
            )
            LOG.debug(f"Sent to SNS Topic: {str(self.topic)}, response: {str(response)}, message: {str(self.message)}, attributes: {str(messageAttributes)}")
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
        except Exception as e:
            LOG.error(f"Failed to send event to SNS Topic: {str(self.topic)}, error:, {str(e)}, message: {str(self.message)}, attributes: {str(messageAttributes)}")
            LOG.error(traceback.format_exc())
            return False

        return False

    def send_to_sqs(self, attributes=None):
        try:
            messageAttributes = {}
            if attributes:
                for attribute in attributes:
                    messageAttributes[attribute] = {
                        'DataType': 'String.Array',
                        'StringValue': json.dumps(attributes[attribute])
                    }

            response = self.client.send_message(
                QueueUrl=self.queueurl,
                MessageBody=json.dumps(self.message),
                MessageAttributes=messageAttributes
            )
            LOG.debug(f"Sent to SQS Queue: {str(self.queueurl)}, response: {str(response)}, message: {str(self.message)}, attributes: {str(messageAttributes)}")
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
        except Exception as e:
            LOG.error(f"Failed to send event to SQS Queue: {str(self.queueurl)}, error:, {str(e)}, message: {str(self.message)}, attributes: {str(messageAttributes)}")
            LOG.error(traceback.format_exc())
            return False

        return False

