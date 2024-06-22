#!/usr/bin/python
#  -*- coding: utf-8 -*-

import ntplib, daqhats, time, os, datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

dq = daqhats.mcc128(0)
the_date = datetime.datetime.now()
datapath = '/home/muonium/data/muon_tagging/segmented/'

directory_path = os.path.join(datapath, the_date.strftime('%Y_%m%d'))

if not os.path.exists(directory_path): os.mkdir(directory_path)
log_path = os.path.join(directory_path, the_date(.strftime('%y%m%d_%H%M%S')



seconds = 1
channel_mask = 0x01
sample_rate = 100000.0
samples = int(sample_rate*seconds)
options = daqhats.OptionFlags.DEFAULT

counter = 0
try:

    for i in range(60):
        tstart = time.time_ns()
        dq.a_in_scan_start(channel_mask, samples, sample_rate, options)
        voltages = dq.a_in_scan_read_numpy(samples, 60)[5]
        tend = time.time_ns()
        timestep = (tend-tstart)/samples

        signal = np.argwhere(voltages < (np.min(voltages)/2)).flatten()
        times = (np.asarray(range(samples))*timestep)[signal]
        times = np.delete(times, np.argwhere(np.ediff1d(times) <= 200*1000) + 1)
        times = times + tstart
        
        for j in range(len(times)):
            log.write(fr'{counter},{times[j]}'+'\n')
            counter += 1
        dq.a_in_scan_cleanup()
    log.close()
except KeyboardInterrupt:
    log.close()
    print('keyboard interrupt: closed the log')
