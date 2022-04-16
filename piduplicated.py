#!/usr/bin/env python3

#----------------------------------------------------------#
#                   == PiDuplicated ==                     #
#                                                          #
#   Check for duplicated files inside 'PiBackup' and/or    #
#   'PiTimelapse' folder in the Backup SSD/HD and          #
#   deletes or informs into '.log' file                    #
#                                                          #
#        https://github.com/richonguzman/PiBackup          #
#                                                          #
# Copyright (C) 2022 Ricardo Guzman richonguzman@gmail.com #
#                                                          #
#----------------------------------------------------------#

import os, time, sys
import RPi.GPIO as GPIO
from hashlib import blake2s

led_pin = 16               # 3mm Red LED in series with 2k2 resistor connected to pin 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setwarnings(False)

path_mounted_disk = '/media/pi/'

def check_connected_disks():
    while len(os.listdir(path_mounted_disk)) == 0:
        GPIO.output(led_pin, False)
        time.sleep(0.5)
        GPIO.output(led_pin, True)
        time.sleep(0.5)
    duplicate_analysis_disk = os.listdir(path_mounted_disk)[0]
    path_duplicate_analysis_disk = os.path.join(path_mounted_disk, duplicate_analysis_disk)
    print("Duplicated File Analysis on Disk : " + duplicate_analysis_disk + '\n')
    return path_duplicate_analysis_disk

def get_hash(archivo):
        m = blake2s(digest_size=32)
        with open(archivo, 'rb') as fp:
            for chunk in fp:
                m.update(chunk)
        return m.hexdigest()

def check_for_log_file(path_ext_disk):
    if os.path.isfile(os.path.join(path_ext_disk, 'duplicated_files.log')):
        n = 1
        path_log = os.path.join(path_ext_disk, 'duplicated_files_' + str(n) + '.log')
        while os.path.isfile(os.path.join(path_ext_disk, 'duplicated_files_' + str(n) + '.log')):
            n += 1
            path_log = os.path.join(path_ext_disk, 'duplicated_files_' + str(n) + '.log')
    else:
        path_log = os.path.join(path_ext_disk, 'duplicated_files.log')
    return path_log

def duplicated_analysis(path_disk):
    time.sleep(1)
    duplicated = False
    if sys.argv[1] == 'log':
        path_log_file = check_for_log_file(path_disk)
    path_file_list = []
    hash_path_file_list = []
    jpg_extension = ('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')
    raw_extension = ('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2',
                     'RW2', 'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG',
                     'ptx', 'PTX', 'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2',
                     'SR2', 'tiff', 'TIFF', 'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')
    video_extension = ('hevc', 'HEVC', 'mkv', 'MKV', 'avi', 'AVI', 'mov', 'MOV', 'wmv',
                       'WMV', 'mp4', 'MP4', 'm4p', 'M4P', 'm4v', 'M4V', 'mpg', 'MPG',
                       'mpeg', 'MPEG', 'lrv', 'LRV')
    time.sleep(0.2)
    if sys.argv[2] == 'j':
        extension = jpg_extension
    elif sys.argv[2] == 'r':
        extension = raw_extension
    elif sys.argv[2] == 'jr':
        extension = jpg_extension + raw_extension
    elif sys.argv[2] == 'jrv':
        extension = jpg_extension + raw_extension + video_extension
    for D, SD, F in os.walk(path_disk):
        for file in F:
            if file.endswith(extension):
                path_file = os.path.join(path_disk, D, file)
                path_file_list.append(path_file)
    path_file_list.sort()
    for x in range(len(path_file_list)):
        hash_file = get_hash(path_file_list[x])
        if hash_file in hash_path_file_list:
            duplicated = True
            if sys.argv[1] == 'log':
                with open(path_log_file,'a') as output_log:
                    output_log.write(path_file_list[x] + '\n')
                print('Duplicated File : ' + path_file_list[x])
            elif sys.argv[1] == 'delete':
                print(path_file_list[x] + ' duplicated and deleted')
                os.remove(path_file_list[x])
        else:
            hash_path_file_list.append(hash_file)
    if not duplicated:
        print("\nNo Duplicated Files Found")
            
def finalize(path_ext_disk):
    counter = 0
    GPIO.output(led_pin, False)
    time.sleep(1)
    while counter < 4:
        GPIO.output(led_pin, True)
        time.sleep(0.1)
        GPIO.output(led_pin, False)
        time.sleep(0.1)
        GPIO.output(led_pin, True)
        time.sleep(0.1)
        GPIO.output(led_pin, False)
        time.sleep(0.1)
        GPIO.output(led_pin, True)
        time.sleep(0.1)
        GPIO.output(led_pin, False)
        time.sleep(0.6)
        counter += 1
#     GPIO.cleanup()
    command = 'sudo eject ' + path_ext_disk
    os.system(command)
    print('\n' + "End (Disk unmounted!)")
            
def start_piduplicated():
    print("*** PiDuplicated ***" + '\n')
    path_external_disk = check_connected_disks()
    duplicated_analysis(path_external_disk)
    finalize(path_external_disk)


####################################### PiDuplicated #######################################
start_piduplicated()