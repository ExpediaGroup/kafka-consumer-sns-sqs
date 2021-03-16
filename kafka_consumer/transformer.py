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
from kafka_consumer.configs.log import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL if LOG_LEVEL else "INFO")
LOG = logging.getLogger(__name__)


class Transformer:
    """Transformer performs event transformation.
        transform_type: Optional. Used to have variations of transformations within the same transformer.
    """
    def __init__(self, transform_type):
        super().__init__()
        self.transform_type = transform_type

    def transform_event(self, data):
        if self.transform_type == "event":
            return self.to_event(data)
        else:
            return None

    def to_event(self, data):
        """Performs event transformation.
        Parameters:
            data: event data on which transformation will be applied
        Returns:
            JSON object
        """
        try:
            severity = data["anomalyResult"]["anomalyLevel"]

            if severity == "NORMAL":
                return None

            event = data["metricData"]['metricDefinition']['tags']['kv']

            if severity == "WEAK":
                event["severity"] = 1
            elif severity == "STRONG":
                event["severity"] = 2

            what = event.get("what", None)
            application = event.get("application", event.get("role"))
            environment = event.get("environment", None)
            elb = event.get("elb", None)
            event["eventtype"] = '_'.join(filter(None, [what, elb, application, environment]))

            if "elb" in event:
                event["resource"] = event.get("elb")
            if "role" in event:
                event["application"] = event.get("role")

            event["source"] = "adaptive-alerting"

            return event

        except Exception as e:
            LOG.error('Error with data transformation', str(e))
            LOG.error(traceback.format_exc())
            return None
