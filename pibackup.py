#!/usr/bin/env python3

#----------------------------------------------------------#
#                     == PiBackup ==                       #
#                                                          #
#   Backup (photography) files from your Camera SD-Card    #
#   into your external SSD/HD with a Raspberry Pi 4        #
#                                                          #
#        https://github.com/richonguzman/PiBackup          #
#                                                          #
# Copyright (C) 2022 Ricardo Guzman richonguzman@gmail.com #
#                                                          #
#----------------------------------------------------------#

import os, exiftool, shutil, psutil, time, sys
from hashlib import blake2s
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
    destination = os.path.join(path_mounted_disk, destination_disk, 'PiBackup')
    if not os.path.isdir(destination):
        os.mkdir(destination)
        print("'PiBackup' folder created")
    print("Source Disk  : " + source_disk)
    print("Backup Disk  : " + destination_disk)
    return source, destination

def creating_file_list(source_path, destination_path, file_type):
    time.sleep(1)
    souce_files = []
    souce_path_files = []
    destination_files = []
    destination_path_files = []
    jpg_extension = ('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')
    raw_extension = ('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2',
                     'RW2', 'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG',
                     'ptx', 'PTX', 'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2',
                     'SR2', 'tiff', 'TIFF', 'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')
    video_extension = ('hevc', 'HEVC', 'mkv', 'MKV', 'avi', 'AVI', 'mov', 'MOV', 'wmv',
                       'WMV', 'mp4', 'MP4', 'm4p', 'M4P', 'm4v', 'M4V', 'mpg', 'MPG',
                       'mpeg', 'MPEG', 'lrv', 'LRV', '360', 'insv', 'INSV')
    if file_type == 'j':
        extension = jpg_extension
    elif file_type == 'r':
        extension = raw_extension
    elif file_type == 'v':
        extension = video_extension
    elif file_type == 'jr':
        extension = jpg_extension + raw_extension
    elif file_type == 'jrv':
        extension = jpg_extension + raw_extension + video_extension
    for D, SD, F in os.walk(source_path):
        for file in F:
            if not file.endswith('DS_Store'):
                if file.endswith((extension)):
                    souce_files.append(file)
                    path_1 = os.path.join(source_path, D, file)
                    souce_path_files.append(path_1)
    for D2, SD2, F2 in os.walk(destination_path):
        for file2 in F2:
            if not file2.endswith('DS_Store'):
                if file2.endswith((extension)):
                    destination_files.append(file2)
                    path_2 = os.path.join(destination_path, D2, file2)
                    destination_path_files.append(path_2)
    return souce_files, souce_path_files, destination_files, destination_path_files

def get_hash(file_to_hash):
        m = blake2s(digest_size=32)
        with open(file_to_hash, 'rb') as fp:
            for chunk in fp:
                m.update(chunk)
        return m.hexdigest()

def list_analysis(source_file_list, source_path_file_list, destination_file_list, destination_path_file_list, path_destination_folder):
    GPIO.output(led_pin, True)
    duplicated = False
    total_weight = 0
    files_to_copy_list = []
    path_files_to_copy_list = []
    for a in range(len(source_file_list)):
        duplicated = False
        file_name, file_extension = os.path.splitext(source_file_list[a])
        for b in range(len(destination_file_list)):
            if duplicated == False:
                if file_name in destination_file_list[b] and destination_file_list[b].endswith(file_extension):
                    if source_file_list[a] == destination_file_list[b]:
                        source_file_size  = os.path.getsize(source_path_file_list[a])
                        destination_file_size = os.path.getsize(destination_path_file_list[b])
                        if source_file_size == destination_file_size:
                            duplicated = True
                        else:
                            n = 1
                            hash_source_file = get_hash(source_path_file_list[a])
                            destination_file_name, destination_file_extension = os.path.splitext(destination_path_file_list[b])
                            while os.path.isfile(destination_file_name[:-1] + str(n) + file_extension):
                                path = os.path.join(destination_file_name[:-1] + str(n) + destination_file_extension)
                                hash_destination_file = get_hash(path)
                                if hash_source_file == hash_destination_file:
                                    duplicated = True
                                n += 1
                    else:
                        n = 1
                        hash_source_file = get_hash(source_path_file_list[a])
                        destination_file_name, destination_file_extension = os.path.splitext(destination_path_file_list[b])
                        while os.path.isfile(destination_file_name[:-1] + str(n) + file_extension):
                            path = os.path.join(destination_file_name[:-1] + str(n) + destination_file_extension)
                            hash_destination_file = get_hash(path)
                            if hash_source_file == hash_destination_file:
                                duplicated = True
                            n += 1
        if not duplicated:
            files_to_copy_list.append(source_file_list[a])
            path_files_to_copy_list.append(source_path_file_list[a])
            total_weight += os.path.getsize(source_path_file_list[a])
    print('\nFiles to copy      : ' + str(len(files_to_copy_list)))
    print('Size of Backup     : ' + str(round((total_weight/1000000000),3)) + ' GB')
        
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        if partition.mountpoint == path_destination_folder.split('/PiBackup')[0]:
            available_space = partition_usage.free/1000000000
            print('Available Space    : ' +str(round(available_space,1)) + ' GB') 
    if (total_weight/1000000000) < available_space:
        return files_to_copy_list, path_files_to_copy_list, len(files_to_copy_list)
    else:
        print("\nNot enough space on 'Backup Disk' to make Backup !")

def list_files_to_copy(file_type):
    source, destination = check_connected_disks()
    source_files, source_path_files, destination_files, destination_path_files = creating_file_list(source, destination, file_type)
    
    files_to_copy = []
    for source_file, source_path_file in zip(source_files, source_path_files):
        file_info = {
            'name': os.path.basename(source_path_file),
            'extension': os.path.splitext(source_path_file)[1],
            'date_modified': time.ctime(os.path.getmtime(source_path_file))
        }
        if file_info['name'] not in destination_files or os.path.getsize(source_path_file) != os.path.getsize(os.path.join(destination_path, file_info['name'])):
            files_to_copy.append(file_info)
    
    return files_to_copy

def copying(files_copy, path_files_copy, destination_names, path_destination_folder, total_files):
    led_counter = 0
    print('\nCopying files...')

    for index, file in enumerate(files_copy):
        current_file = os.path.basename(path_files_copy[index])
        print(f"Copying {current_file} ({index + 1}/{total_files})...")

        # Calculate and display the progress percentage
        progress_percentage = ((index + 1) / total_files) * 100
        print(f"Progress: {progress_percentage:.2f}%")

        n_process = False
        for destination_file in destination_names:
            if file == destination_file:
                n_process = True
                break

        if n_process:
            n = 1
            file_name, file_extension = os.path.splitext(file)
            new_file_name = f"{file_name}_{n}{file_extension}"
            while new_file_name in destination_names:
                n += 1
                new_file_name = f"{file_name}_{n}{file_extension}"

            destination_path = os.path.join(path_destination_folder, new_file_name)
            shutil.copy2(path_files_copy[index], destination_path)
            destination_names.append(new_file_name)
        else:
            destination_path = os.path.join(path_destination_folder, file)
            shutil.copy2(path_files_copy[index], destination_path)
            destination_names.append(file)

        # Toggle LED to indicate progress
        led_counter = (led_counter + 1) % 2
        GPIO.output(led_pin, led_counter == 0)
        time.sleep(0.05)

                
def sort_files_by_exif_data(path_folders_to_check):
    exif_files_counter = 0
    led_counter = 0
    excludes = os.listdir(path_folders_to_check)
    for dirName, subdirList, fileList in os.walk(path_folders_to_check):
        subdirList[:] = [d for d in subdirList if d not in excludes]
        if len(fileList) > 0:
            print("\nprocessing Exif Data from files...")
            for fname in fileList:
                path_source_exif_file = os.path.join(path_folders_to_check, dirName, fname)
                with exiftool.ExifToolHelper() as et:
                    make = et.get_tags(path_source_exif_file, 'Make')
                    model = et.get_tags(path_source_exif_file, 'Model')
                    camera_company = make[0]['EXIF:Make']
                    camera_model = model[0]['EXIF:Model']
                    if camera_company==None:
                        new_folder = os.path.join(path_folders_to_check ,'other_files')
                        new_destination_path = os.path.join(new_folder, fname)
                        if not os.path.isdir(new_folder):
                            os.mkdir(new_folder)
                        shutil.move(path_source_exif_file, new_destination_path)
                    else:
                        new_folder = os.path.join(path_folders_to_check, str(camera_company) + " " + str(camera_model))
                        new_destination_path = os.path.join(new_folder, fname)
                        if not os.path.isdir(new_folder):
                            os.mkdir(new_folder)
                        shutil.move(path_source_exif_file, new_destination_path)
                    if led_counter == 0:
                        GPIO.output(led_pin, False)
                        time.sleep(0.05)
                        led_counter = 1
                    else:
                        GPIO.output(led_pin, True)
                        time.sleep(0.05)
                        led_counter = 0
                exif_files_counter += 1
        print("("+ str(exif_files_counter) + " EXIF Data from files processed)")

def separate_files_by_extension(path_folders_to_check):
    jpg_extension = ('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')
    raw_extension = ('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2', 'RW2',
                     'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG', 'ptx', 'PTX',
                     'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2', 'SR2', 'tiff', 'TIFF',
                     'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')
    jpg_counter = 0
    raw_counter = 0
    folders_to_check = os.listdir(path_folders_to_check)
    folders_to_check.sort()
    for x in range(len(folders_to_check)):
        folder_being_checked = os.path.join(path_folders_to_check, folders_to_check[x])
        excludes = os.listdir(folder_being_checked)
        for D, sD, f in os.walk(folder_being_checked):
            sD[:] = [d for d in sD if d not in excludes]
            for file in f:
                path = os.path.join(folder_being_checked, file)
                if file.endswith((jpg_extension)):
                    if jpg_counter == 0:
                        path_jpg_folder = os.path.join(folder_being_checked, 'JPG')
                        if not os.path.isdir(path_jpg_folder):
                            os.mkdir(path_jpg_folder)
                        jpg_counter = 1
                    shutil.move(path, os.path.join(path_jpg_folder, file))
                if file.endswith((raw_extension)):
                    if raw_counter == 0:
                        path_raw_folder = os.path.join(folder_being_checked, 'RAW')
                        if not os.path.isdir(path_raw_folder):
                            os.mkdir(path_raw_folder)
                        raw_counter = 1
                    shutil.move(path, os.path.join(path_raw_folder, file))
    print("\n(files separated by extension)")
    
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
    command_2 = 'sudo eject ' + path_destination_dsk.split('/PiBackup')[0]
    os.system(command_1)
    time.sleep(0.5)
    os.system(command_2)
    print('\n' + "End (Disks unmounted!)")
    
def start_pibackup():
    print("***** PiBackup *****" + '\n')
    path_source_disk, path_destination_disk = check_connected_disks()    
    s_files, path_s_files, d_files, path_d_files = creating_file_list(path_source_disk, path_destination_disk, sys.argv[1])
    files_to_copy, path_files_to_copy, total_files_to_copy = list_analysis(s_files, path_s_files, d_files, path_d_files, path_destination_disk)
    if len(files_to_copy) == 0:
        print("\nNo new files to backup")
    else:
        copying(files_to_copy, path_files_to_copy, d_files, path_destination_disk, total_files_to_copy)
        sort_files_by_exif_data(path_destination_disk)
        separate_files_by_extension(path_destination_disk)
        finalize(path_source_disk, path_destination_disk)
    
    
####################################### PiBackup #######################################
if __name__ == "__main__":
    start_pibackup()