#!/usr/bin/env bash
printf "Configuring localstack components..."

readonly LOCALSTACK_SNS_URL=http://localstack:4566


sleep 5;

set -x

aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
echo "[default]" > ~/.aws/config
echo "region = us-west-2" >> ~/.aws/config
echo "output = json" >> ~/.aws/config

aws --endpoint $LOCALSTACK_SNS_URL sns create-topic --name TEST_SNS_TOPIC

printf "Sample data begin..."
# create tmp directory to put sample data after chunking
mkdir -p /tmp/localstack/data

set +x
