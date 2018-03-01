#!/bin/bash

ps aux|grep -v grep|grep start-local|awk '{print $2}'|xargs kill -9