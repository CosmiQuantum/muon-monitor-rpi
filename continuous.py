#!/usr/bin/python
#  -*- coding: utf-8 -*-

import ntplib, daqhats, time, os, datetime
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

datapath = '/home/muonium/data/muon_tagging/continuous/'
run_time = 3595 





def continuous_read(seconds=5, log_path=None, save=True):
    """
    Reads out data from the nim logic, onto the raspberry pi. This is saved as a json file. 
    args:
        Seconds (float): number of seconds that the program will run for.
        log_path (str): The path that the data will be saved along
        save (bool): keyword specifying if the data should be saved
    """
    t_start = time.time()
    while seconds > time.time() - t_start:
        voltage = dq.a_in_read(0)
        if (voltage < -0.4) and save:
            log = open(log_path, 'a+')
            log.write(fr'0,0,{time.time_ns()}'+'\n')
            log.close()

def format_log(temp_path, log_path):
    """
    Formats the log to the data from the temporary file, and also removes certain events which are especially close together, as we don't have true sensitivity down to a certain scale. Removes temp file when done. 
    args:
        temp_path (str): Path to the temporary file which is written during constant read out. This is done for speed, reducing the amount of computation time it takes to write. 
        log_path (str): The path that the data will be saved along
    """
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
    """
    Initializes the log file with the correct headers.
    args:
        path (str): path to the log file to initialize

    """
    log = open(path, 'a+')
    log.write(fr'event,t_muon,t_muon_ns'+'\n')
    log.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


dq = daqhats.mcc128(0)
the_date = datetime.datetime.now()

directory_path = os.path.join(datapath, the_date.strftime('%Y_%m%d'))


if not os.path.exists(directory_path): os.mkdir(directory_path)


log_path = os.path.join(directory_path,the_date.strftime('%y%m%d_%H%M%S') + '.csv')
temp_path = 'temp.log'
initialize_log(log_path)
if not os.path.exists(temp_path): initialize_log(temp_path)

try:
    print('\n')
    print(the_date)
    print('made it through to first continuous_read')
    continuous_read(seconds=1, save=False)
    print('Beginning continuous scan...')
    continuous_read(seconds=run_time, log_path=temp_path, save=True)
    print('Continuous scan complete.')
    format_log(temp_path, log_path)
except KeyboardInterrupt:
    format_log(temp_path, log_path)
    print('KeyboardInterrupt: formatted and exited')
