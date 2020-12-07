sudo yum install -y aws-kinesis-agent
chmod a+x walmart/LogGenerator.py
sudo mkdir /var/log/cadabra
sudo cp -rf kinesis-data-firehose/agent.json /etc/aws-kinesis
sudo service aws-kinesis-agent restart
sudo chkconfig aws-kinesis-agent on
tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log
