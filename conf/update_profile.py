#!/usr/bin/env python3

import os

current_folder = os.getcwd() + '/'

def start_update():
    with open('/etc/profile','r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            with open(current_folder + 'conf/profile','a') as output_file:
                output_file.write(line)
    input_file.close()
    with open(current_folder + 'conf/profile','a') as output_file:
        output_file.write('sudo python3 /home/pi/PiBackup/pibackup_web.py &')
    output_file.close()
        
############ UPDATE_PROFILE ############
start_update()