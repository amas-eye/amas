#!/usr/bin/env bash

cd /opt/amas/argus_statistics
nohup python app.py --start &

tail -f /opt/amas/argus_statistics/logs/app.log