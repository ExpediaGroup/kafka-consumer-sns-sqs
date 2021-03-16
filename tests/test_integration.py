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

from kafka_consumer.transformer import Transformer
from kafka_consumer.processor import KafkaProcessor
import pytest
import logging
import os

logging.basicConfig(level="DEBUG")
LOG = logging.getLogger(__name__)

pytest_plugins = ["docker_compose"]


# Invoking this fixture: 'function_scoped_container_getter' starts all container services
@pytest.fixture(scope="function")
def wait_for_dependencies(function_scoped_container_getter):
    """Wait for the SNS to become responsive"""

    os.system("./docker/kafkaconsumer/wait-for-dependencies.sh")


def test_integration(caplog, wait_for_dependencies):
    with caplog.at_level(logging.DEBUG):
        transform = Transformer(transform_type="event")
        processor = KafkaProcessor(transformer=transform.transform_event, transform_type="event", consumer_type="sns")
        processor.process_message()
    assert "Sent to SNS Topic: arn:aws:sns:us-west-2:000000000000:TEST_SNS_TOPIC" in caplog.text

