sudo yum install -y aws-kinesis-agent
wget http://media.sundog-soft.com/AWSBigData/LogGenerator.zip
unzip LogGenerator.zip
chmod a+x LogGenerator.py
sudo mkdir /var/log/cadabra
cd /etc/aws-kinesis
sudo nano agent.json
sudo service aws-kinesis-agent start
sudo chkconfig aws-kinesis-agent on
cd ~
sudo ./LogGenerator.py 500000
cd /var/log/cadabra
tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log

# firehose endpoint : firehose.us-east-1.amazonaws.com

# "filePattern": "/var/log/cadabra/*log"
