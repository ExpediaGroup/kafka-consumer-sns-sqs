import os

KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")
GROUP_ID = os.environ.get("GROUP_ID")
BOOTSTRAP_SERVERS = os.environ.get("BOOTSTRAP_SERVERS")
AUTO_OFFSET_RESET = os.environ.get("AUTO_OFFSET_RESET")
CONSUMER_TIMEOUT_MS = os.environ.get("CONSUMER_TIMEOUT_MS")
