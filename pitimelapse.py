#!/usr/bin/env python3

#----------------------------------------------------------#
#                    == PiTimelapse ==                     #
#                                                          #
#  Sort and rename all the photographs of a Timelapse to   #
#  help with importing, processing and making a backup     #
#                                                          #
#        https://github.com/richonguzman/PiBackup          #
#                                                          #
# Copyright (C) 2022 Ricardo Guzman richonguzman@gmail.com #
#                                                          #
#----------------------------------------------------------#

import os, time, exiftool, shutil, sys
from datetime import datetime
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
    destination = os.path.join(path_mounted_disk, destination_disk)
    while len(os.listdir(path_mounted_disk)) == 1:
        GPIO.output(led_pin, True)
        time.sleep(0.1)
        GPIO.output(led_pin, False)
        time.sleep(0.1)
    if destination_disk == os.listdir(path_mounted_disk)[0]:
        source_disk = os.listdir(path_mounted_disk)[1]
    else:
        source_disk = os.listdir(path_mounted_disk)[0]
    source = os.path.join(path_mounted_disk, source_disk)
    destination = os.path.join(path_mounted_disk, destination_disk, 'PiTimelapse')
    if not os.path.isdir(destination):
        os.mkdir(destination)
        print("'PiTimelapse' folder created")   
    print("Source Disk  : " + source_disk)
    print("Backup Disk  : " + destination_disk)
    return source, destination

def copy_timelapse_sd_to_ssd(path_timelapse_source, path_timelapse_destination):
    time.sleep(1)
    led_counter = 0
    files_being_processed = [] 
    jpg_extension = ('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')
    raw_extension = ('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2',
                     'RW2', 'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG',
                     'ptx', 'PTX', 'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2',
                     'SR2', 'tiff', 'TIFF', 'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')
    if sys.argv[1] == 'j':
        extension = jpg_extension
    elif sys.argv[1] == 'r':
        extension = raw_extension
    elif sys.argv[1] == 'jr':
        extension = jpg_extension + raw_extension
    GPIO.output(led_pin, True)
    excludes = os.listdir(path_timelapse_destination)
    for D, sD, f in os.walk(path_timelapse_destination):
        sD[:] = [d for d in sD if d not in excludes]
        for file_in_folder in f:
            if file_in_folder.endswith(extension):
                files_being_processed.append(file_in_folder)
    for D, sD, F in os.walk(path_timelapse_source):
        for file in F:
            if file.endswith(extension):
                path_source_file = os.path.join(path_timelapse_source, D, file)
                if file in files_being_processed:
                    size_source_file = os.path.getsize(path_source_file)
                    for x in range(len(files_being_processed)):
                        if file == files_being_processed[x]:
                            path_file_in_folder = os.path.join(path_timelapse_destination, files_being_processed[x])
                            size_file_in_folder = os.path.getsize(path_file_in_folder)
                            if size_source_file != size_file_in_folder:
                                shutil.copy2(path_source_file, os.path.join(path_timelapse_destination, file))
                                files_being_processed.append(file)
                                if led_counter == 0:
                                    GPIO.output(led_pin, False)
                                    time.sleep(0.05)
                                    led_counter = 1
                                else:
                                    GPIO.output(led_pin, True)
                                    time.sleep(0.05)
                                    led_counter = 0
                else:
                    shutil.copy2(path_source_file, os.path.join(path_timelapse_destination, file))
                    files_being_processed.append(file)
                    if led_counter == 0:
                        GPIO.output(led_pin, False)
                        time.sleep(0.05)
                        led_counter = 1
                    else:
                        GPIO.output(led_pin, True)
                        time.sleep(0.05)
                        led_counter = 0
    if len(files_being_processed) > 0:
        date_and_camera_model = oldest_file_exif_data(path_timelapse_destination)
        new_timelapse_date_folder = os.path.join(path_timelapse_destination, date_and_camera_model)
        organize_folder(path_timelapse_destination, new_timelapse_date_folder)
        extension_separator(new_timelapse_date_folder)
        sequence_order(new_timelapse_date_folder)
        print(date_and_camera_model)
        print('(' + str(len(files_being_processed)) + ' files processed)')

def oldest_file_exif_data(path_destination):
    first_data = True
    saved_date = 0
    saved_path = ""
    excludes = os.listdir(path_destination)
    for D, sD, f in os.walk(path_destination):
        sD[:] = [d for d in sD if d not in excludes]
        for file in f:
            path_file = os.path.join(path_destination, D, file)
            file_date = os.path.getmtime(path_file)
            if first_data:
                saved_path = path_file
                saved_date = file_date
                first_data = False
            if saved_date > file_date:
                saved_path = path_file
                saved_date = file_date
        formated_date = datetime.fromtimestamp(saved_date).strftime('%Y_%m_%d_%Hh%Mm')
        with exiftool.ExifToolHelper() as et:
            make = et.get_tags(saved_path, 'Make')
            model = et.get_tags(saved_path, 'Model')
            camera_company = make[0]['EXIF:Make']
            camera_model = model[0]['EXIF:Model'] 
            if make==None:
                date_and_camera_info = "No_Date_Info"
            else:
                date_and_camera_info = formated_date + ' ' + str(camera_company) +' ' + str(camera_model)  
            return date_and_camera_info

def organize_folder(path_pitimelapse_folder, new_folder):
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)
    excludes = os.listdir(path_pitimelapse_folder)
    for D, sD, F in os.walk(path_pitimelapse_folder):
        sD[:] = [d for d in sD if d not in excludes]
        for file in F:
            path_file = os.path.join(path_pitimelapse_folder, D, file)
            new_path_file = os.path.join(new_folder, file)
            shutil.move(path_file, new_path_file)          

def extension_separator(path_timelapse_folder):
    jpg_folder = False
    raw_folder = False
    jpg_extension = ('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')
    raw_extension = ('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2', 'RW2',
                     'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG', 'ptx', 'PTX',
                     'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2', 'SR2', 'tiff', 'TIFF',
                     'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')
    excludes = os.listdir(path_timelapse_folder)
    for D, sD, f in os.walk(path_timelapse_folder):
        sD[:] = [d for d in sD if d not in excludes]
        for file in f:
            path_file = os.path.join(D, file)
            if file.endswith((jpg_extension)):
                path_jpg_folder = os.path.join(path_timelapse_folder, 'JPG')
                if not jpg_folder:
                    if not os.path.isdir(path_jpg_folder):
                        os.mkdir(path_jpg_folder)
                        jpg_folder = True
                shutil.move(path_file, os.path.join(path_jpg_folder, file))
            elif file.endswith((raw_extension)):
                path_raw_folder = os.path.join(path_timelapse_folder, 'RAW')
                if not raw_folder:
                    if not os.path.isdir(path_raw_folder):
                        os.mkdir(path_raw_folder)
                        raw_folder = True
                shutil.move(path_file, os.path.join(path_raw_folder, file))
        
def sequence_order(path_folder):
    if os.path.isdir(os.path.join(path_folder, 'JPG')):
        file_date_list = []
        path_new_sequence = os.path.join(path_folder,'JPG')
        who_are_they = os.listdir(path_new_sequence)
        for z in range(len(who_are_they)):
            file_date = os.path.getmtime(os.path.join(path_new_sequence, who_are_they[z]))
            file_date_list.append(file_date)
        file_date_list.sort()
        counter = 1
        for y in range(len(who_are_they)):
            searched_file_date = file_date_list[y]
            for D, sD, f in os.walk(path_new_sequence):
                for file in f:
                    if not file.startswith(('Timelapse')):
                        path_file = os.path.join(path_new_sequence, file)
                        posible_file_date = os.path.getmtime(path_file)
                        if searched_file_date == posible_file_date:
                            current_folder, file_name = os.path.split(path_file)
                            string_counter = str(counter)
                            sequence_counter = string_counter.zfill(4)
                            new_file_name = 'Timelapse_' + sequence_counter + "_" + file_name
                            os.rename(path_file, os.path.join(path_new_sequence, new_file_name))
                            counter += 1
                            GPIO.output(led_pin, True)            
    if os.path.isdir(os.path.join(path_folder, 'RAW')):
        file_date_list = []
        path_new_sequence = os.path.join(path_folder, 'RAW')
        who_are_they = os.listdir(path_new_sequence)
        for z in range(len(who_are_they)):
            file_date = os.path.getmtime(os.path.join(path_new_sequence, who_are_they[z]))
            file_date_list.append(file_date)
        file_date_list.sort()
        counter = 1
        for y in range(len(who_are_they)):
            searched_file_date = file_date_list[y]
            for D, sD, f in os.walk(path_new_sequence):
                for file in f:
                    if not file.startswith(('Timelapse')):
                        path_file = os.path.join(path_new_sequence, file)
                        posible_file_date = os.path.getmtime(path_file)
                        if searched_file_date == posible_file_date:
                            current_folder, file_name = os.path.split(path_file)
                            string_counter = str(counter)
                            sequence_counter = string_counter.zfill(4)
                            new_file_name = 'Timelapse_' + sequence_counter + "_" + file_name
                            os.rename(path_file, os.path.join(path_new_sequence, new_file_name))
                            counter += 1
                            GPIO.output(led_pin, True)
    print("\nTimelapse Sequence Ready")

def finalize(path_source_dsk, path_destination_dsk):
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
    command_1 = 'sudo eject ' + path_source_dsk
    command_2 = 'sudo eject ' + path_destination_dsk.split('/PiTimelapse')[0]
    os.system(command_1)
    time.sleep(0.5)
    os.system(command_2)
    print('\n' + "End (Disks unmounted!)")

def start_pitimelapse():
    print("*** PiTimelapse ***" + '\n')
    path_source_disk, path_destination_disk = check_connected_disks()
    copy_timelapse_sd_to_ssd(path_source_disk, path_destination_disk)
    finalize(path_source_disk, path_destination_disk)


####################################### PiTimelapse #######################################
start_pitimelapse()