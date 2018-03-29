#!/usr/bin/env bash

cd /opt/amas/argus_alert/bin
./start-local.py

hostname=`hostname`
tail -f /opt/amas/argus_alert/logs/root@${hostname}.log