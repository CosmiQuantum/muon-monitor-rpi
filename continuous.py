#!/usr/bin/python
#  -*- coding: utf-8 -*-

import ntplib, daqhats, time, os, datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def continuous_read(seconds=5, log_path=None, save=True):
	t_start = time.time()
	while seconds > time.time() - t_start:
		voltage = dq.a_in_read(0)
		if (voltage < -0.4) and save:
			log = open(log_path, 'a+')
			log.write(fr'0,0,{time.time_ns()}'+'\n')
			log.close()

def format_log(temp_path, log_path):
	temp_file = pd.read_csv(temp_path)
	log_file = pd.read_csv(log_path)
	times = np.delete(temp_file['t_muon_ns'], np.argwhere(np.ediff1d(temp_file['t_muon_ns']) <= 200*1000) + 1)
	new_log = pd.DataFrame()
	new_log['event'] = np.asarray(range(len(np.append(log_file['t_muon'], times))))
	new_log['t_muon'] = np.append(log_file['t_muon'], pd.to_datetime(times).astype('str'))
	new_log['t_muon_ns'] = np.append(log_file['t_muon_ns'], times)
	
	new_log.to_csv(log_path, index=False)
	os.remove(temp_path)
	
def initialize_log(path):
	log = open(path, 'a+')
	log.write(fr'event,t_muon,t_muon_ns'+'\n')
	log.close()
	
dq = daqhats.mcc128(0)
the_date = time.gmtime()
log_path = fr'{the_date[1]:02d}_{the_date[2]:02d}_{the_date[0]:04d}.csv'
temp_path = 'temp.log'

if not os.path.exists(temp_path):
	initialize_log(temp_path)
if not os.path.exists(log_path):
	initialize_log(log_path)

continuous_read(seconds=1, save=False)
print('Beginning continuous scan...')
continuous_read(seconds=60, log_path=temp_path, save=True)
print('Continuous scan complete.')
format_log(temp_path, log_path)

