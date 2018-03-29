#!/usr/bin/env bash

# start agent manager
cd /opt/amas/argus_collector/web
nohup python app.py --start &

# start agent
cd /opt/amas/argus_collector
./tcollector start -D

tail -f logs/collector.log