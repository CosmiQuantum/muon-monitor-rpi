#!/usr/bin/bash

python /home/muonium/muon-monitor-rpi/continuous.py >> /home/muonium/Recording_logs/$(date '+%Y_%m')/outputs_$(date '+%Y_%m%d').txt 

