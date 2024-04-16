#!/usr/bin/python
#  -*- coding: utf-8 -*-

import ntplib, daqhats, time, os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

dq = daqhats.mcc128(0)
the_date = time.gmtime()
log_path = fr'{the_date[1]:02d}_{the_date[2]:02d}_{the_date[0]:04d}_segmented.csv'

if os.path.exists(log_path):
	log = open(log_path, 'a+')
else:
	log = open(log_path, 'a+')
	log.write(fr'event,t_muon'+'\n')

seconds = 1
channel_mask = 0x01
sample_rate = 100000.0
samples = int(sample_rate*seconds)
options = daqhats.OptionFlags.DEFAULT

counter = 0
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
