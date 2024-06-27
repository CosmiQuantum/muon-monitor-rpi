#! /usr/bin/bash

sshpass -p "<>" rsync -ae muonium@192.168.0.112:/home/muonium/data/muon_tagging/$(date '+%Y_%m%d')/$(date '+%y%m%d')_*.csv /home/louduser/cveihmeyer/test_drop/
