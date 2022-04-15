#!/usr/bin/env python3

#----------------------------------------------------------#
#                     == PiClone ==                        #
#                                                          #
#    Clone every file from 'PiBackup' or 'PiTimelapse'     #
#    folder to your Backup SSD/HD to another SSD/HD        #
#                                                          #
#        http://github.com/richonguzman/PiBackup           #
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
    destination_disk = os.listdir(path_mounted_disk)[0]
    destination = path_mounted_disk + destination_disk
    while len(os.listdir(path_mounted_disk)) == 1:
        GPIO.output(led_pin, True)
        time.sleep(0.1)
        GPIO.output(led_pin, False)
        time.sleep(0.1)
    if destination_disk == os.listdir(path_mounted_disk)[0]:
        source_disk = os.listdir(path_mounted_disk)[1]
    else:
        source_disk = os.listdir(path_mounted_disk)[0]
    source = path_mounted_disk + source_disk
    destination = path_mounted_disk + destination_disk
    print("Source Disk  : " + source_disk)
    print("Backup Disk  : " + destination_disk + "\n")
    return source, destination

def clone(path_source, path_destination):
    GPIO.output(led_pin, True)
    time.sleep(1)
    if sys.argv[1] == 'bk':
        folders_to_clone = ['/PiBackup']
    elif sys.argv[1] == 'tm':
        folders_to_clone = ['/PiTimelapse']
    elif sys.argv[1] == 'bktm':
        folders_to_clone = ['/PiBackup', '/PiTimelapse']
    for x in range(len(folders_to_clone)):
        path_source_clone = path_source + folders_to_clone[x]
        path_destination_clone = path_destination + folders_to_clone[x]
        if os.path.isdir(path_source_clone):
            if not os.path.isdir(path_destination_clone):
                os.mkdir(path_destination_clone)
#                 print(path_destination_clone + " folder created")
            clone_command= 'rsync -au '+ path_source_clone + "/ " + path_destination_clone
            print("PiClone '" + folders_to_clone[x][1:] + "' folder ")
            os.system(clone_command)
            print("('"+ folders_to_clone[x][1:] +"' cloned)\n")
        else:
            print("'" + folders_to_clone[x][1:] + "' folder does not exist in Source Disk\n")        
        
def finalize(path_source_dsk, path_destination_dsk):
    counter = 0
    while counter < 4:
        GPIO.output(led_pin, False)
        time.sleep(0.8)
        GPIO.output(led_pin, True)
        time.sleep(0.8)
        counter += 1
    GPIO.cleanup()
    command_1 = 'sudo eject ' + path_source_dsk
    command_2 = 'sudo eject ' + path_destination_dsk
    os.system(command_1)
    time.sleep(0.5)
    os.system(command_2)
    print('\n' + "End (Disk unmounted!)")

def start_piclone():
    print("***** PiClone *****" + '\n')
    path_source_disk, path_destination_disk = check_connected_disks()
    clone(path_source_disk, path_destination_disk)
    finalize(path_source_disk, path_destination_disk)


####################################### PiClone #######################################
start_piclone()