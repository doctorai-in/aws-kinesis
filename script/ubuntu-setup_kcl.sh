#!/bin/bash

AGENT_VERSION=1.1.4
JAVA_START_HEAP=256m
JAVA_MAX_HEAP=512m
LOG_LEVEL=INFO
WORK_DIR=$PWD

# Installation
sudo apt update
sudo apt-get install -y default-jre default-jdk
curl -LO https://github.com/awslabs/amazon-kinesis-agent/archive/${AGENT_VERSION}.tar.gz
tar xvzf ${AGENT_VERSION}.tar.gz
rm ${AGENT_VERSION}.tar.gz 
mv amazon-kinesis-agent-${AGENT_VERSION} amazon-kinesis-agent
cd amazon-kinesis-agent
sudo ./setup --install

# Some setup
mkdir -p /tmp/kinesis
sudo cp $WORK_DIR/agent.json /etc/aws-kinesis/agent.json

# Starting service and tailing log
sudo service aws-kinesis-agent start
sleep 10 
tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log

