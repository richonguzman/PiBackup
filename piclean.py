#!/usr/bin/env python3

#----------------------------------------------------------#
#                     == PiClean ==                        #
#                                                          #
#  Clean(Delete) all JPG files in PiBackup or PiTimelapse  #
#  folders in the external Backup SSD/HD                   #
#                                                          #
#        https://github.com/richonguzman/PiBackup          #
#                                                          #
# Copyright (C) 2022 Ricardo Guzman richonguzman@gmail.com #
#                                                          #
#----------------------------------------------------------#

import os, time, sys
import RPi.GPIO as GPIO

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
    disk_to_clean = os.listdir(path_mounted_disk)[0]
    path_disk_to_clean = os.path.join(path_mounted_disk, disk_to_clean)
    print("Disk to be Cleaned  : " + disk_to_clean + '\n')
    return path_disk_to_clean

def cleaning(path_cleaned):
    time.sleep(1)
    GPIO.output(led_pin, False)
    folders_to_clean = []
    if sys.argv[1] == 'bk':
        folders_to_clean = ['PiBackup']
    elif sys.argv[1] == 'tm':
        folders_to_clean = ['PiTimelapse']
    elif sys.argv[1] == 'bktm':
        folders_to_clean = ['PiBackup', 'PiTimelapse']
    else:
        print("Folders to be cleaned not in disk")
    all_folders_counter = [0,0]
    all_folders_weight = [0,0]
    for x in range(len(folders_to_clean)):
        counter = 0
        folder_weight = 0
        path_clean_folder = os.path.join(path_cleaned, folders_to_clean[x])
        if os.path.isdir(path_clean_folder):
            for D, sD, F in os.walk(path_clean_folder):
                for file in F:
                    path_file_to_clean = os.path.join(path_clean_folder, D, file)
                    if file.endswith(('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')):
                        counter += 1
                        file_weight = os.path.getsize(path_file_to_clean)
                        folder_weight += file_weight
                        os.remove(path_file_to_clean)
            all_folders_counter[x] = counter
            all_folders_weight[x] = round(folder_weight/1000000000,2)
            print(str(all_folders_counter[x]) + " JPG files deleted (" + str(all_folders_weight[x]) + " GB)")
        else:
            print(path_clean_folder + " folder does not exists") 
    
def finalize(path_clean_disk):
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
    command = 'sudo eject ' + path_clean_disk
    os.system(command)
    print('\n' + "End (Disk unmounted!)")

def start_piclean():
    print("***** PiClean *****" + '\n')
    path_disk_to_be_cleaned = check_connected_disks()
    cleaning(path_disk_to_be_cleaned)
    finalize(path_disk_to_be_cleaned)         


####################################### PiClean #######################################
start_piclean()