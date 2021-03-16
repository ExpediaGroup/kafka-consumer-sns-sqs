#!/usr/bin/env bash

if [ ${LOCAL_STACK:-False} = "True" ] ; then 
        /app/kafka-consumer-sns-sqs/wait-for-dependencies.sh ; 
fi
