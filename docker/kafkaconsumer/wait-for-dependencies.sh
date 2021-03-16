#!/usr/bin/env bash

echo "Waiting for SNS at address ${AWS_ENDPOINT_URL}/health, attempting every 5s"
until $(curl --silent --fail ${AWS_ENDPOINT_URL}/health | grep "\"sns\": \"running\"" > /dev/null); do
    printf '.'
    sleep 5
done
echo ' Success: Reached SNS'
