#!/usr/bin/env bash

cd /opt/amas/argus-web/server
npm run start
tail -f logs/pm_com.log
