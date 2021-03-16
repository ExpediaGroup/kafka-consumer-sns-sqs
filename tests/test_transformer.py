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

import unittest
import json
from kafka_consumer.transformer import Transformer


class Test_Transformer(unittest.TestCase):

    def test_transformer(self):
        input_event = self.get_test_event()
        transform = Transformer(transform_type="event")
        transformed_event = transform.to_event(input_event)
        self.assertEqual(transformed_event["severity"], 2)
        self.assertEqual(transformed_event["environment"], "testenv")

    def get_test_event(self):
        with open("tests/test_data.json") as fp:
            test_event = json.load(fp)
        return test_event

