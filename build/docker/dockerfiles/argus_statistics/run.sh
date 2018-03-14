#!/usr/bin/env bash

cd /opt/amas/argus_statistics
nohup python start_dashboard.py --start &

tail -f /opt/amas/argus_statistics/logs/statistics.log