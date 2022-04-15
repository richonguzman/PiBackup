#!/usr/bin/env python3

#----------------------------------------------------------#
#                    == PiTimelapse ==                     #
#                                                          #
#  Sort and rename all the photographs of a Timelapse to   #
#  help with importing, processing and making a backup     #
#                                                          #
#        http://github.com/richonguzman/PiBackup           #
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
    if not os.path.isdir(destination + '/PiTimelapse/'):
        os.mkdir(destination + '/PiTimelapse/')
        print("'PiTimelapse' folder created")
    print("Source Disk  : " + source_disk)
    print("Backup Disk  : " + destination_disk)
    return source, destination

def copy_timelapse_sd_to_ssd(path_timelapse_source, path_timelapse_destination):
#     print('\n' + "copiando...")
    copied_counter = 0
    duplicated_counter = 0
    led_counter = 0
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
    for D, sD, f in os.walk(path_timelapse_source):
        for fname in f:
            if fname.endswith(extension):
                path = os.path.join(path_timelapse_source, D, fname)
                duplicado = revision_duplicado_carpeta_destino_base(path, fname, path_timelapse_destination)
                if duplicado == 2:
                    duplicated_counter += 1
                else:
                    shutil.copy2(path, path_timelapse_destination + '/PiTimelapse/' + fname)
                    copied_counter += 1
                    if led_counter == 0:
                        GPIO.output(led_pin, False)
                        time.sleep(0.05)
                        led_counter = 1
                    else:
                        GPIO.output(led_pin, True)
                        time.sleep(0.05)
                        led_counter = 0
    print(str(copied_counter) + " files copied (" + str(duplicated_counter) + " duplicated)")
    fecha_con_equipo = exif_mas_antiguo(path_timelapse_destination + '/PiTimelapse/')
    carpeta_nueva = path_timelapse_destination + fecha_con_equipo
    reordenar_carpeta(path_timelapse_destination, carpeta_nueva)


def exif_mas_antiguo(path_destination):
    guardar = 0
    fecha_guardada = 0
    path_guardado = ""
    excludes = os.listdir(path_destination)
    for D, sD, f in os.walk(path_destination):
        sD[:] = [d for d in sD if d not in excludes]
        if len(f) == 0:
            print("no hay archivos nuevos")
            fecha_y_equipo = ""
            return fecha_y_equipo
        else:
            for file in f:
                path = os.path.join(path_destination, D, file)
                fecha_archivo = os.path.getmtime(path)
                if guardar == 0:
                    path_guardado = path
                    fecha_guardada = fecha_archivo
                    guardar = 1
                if fecha_guardada > fecha_archivo:
                    path_guardado = path
                    fecha_guardada = fecha_archivo
            fecha_corregida = datetime.fromtimestamp(fecha_guardada).strftime('%Y_%m_%d_%Hh%Mm')
            with exiftool.ExifTool() as et:
                make = et.get_tag('EXIF:Make', path_guardado)
                model = et.get_tag('EXIF:Model', path_guardado)
                if make==None:
                    fecha_y_equipo = ""
                else:
                    fecha_y_equipo = fecha_corregida + ' ' + str(make) +' ' + str(model) + '/'  
                return fecha_y_equipo


def reordenar_carpeta(path_destino, nueva_carpeta):
#     print("reordenando... ")
    if not os.path.isdir(nueva_carpeta):
        os.mkdir(nueva_carpeta)
    excludes = os.listdir(path_destino)
    for D, sD, f in os.walk(path_destino):
        sD[:] = [d for d in sD if d not in excludes]
        for file in f:
            path = os.path.join(path_destino, D, file)
            shutil.move(path, nueva_carpeta + file)
    separar_por_extension(nueva_carpeta)            


def separar_por_extension(nueva_carpeta):
#     print("separando por extension...")
    contador_jpg = 0
    contador_raw = 0
    excludes = os.listdir(nueva_carpeta)
    for D, sD, f in os.walk(nueva_carpeta):
        sD[:] = [d for d in sD if d not in excludes]
        for file in f:
            path = os.path.join(nueva_carpeta + file)
            if file.endswith(('jpg','JPG')):
                if contador_jpg == 0:
                    path_jpg = nueva_carpeta + 'JPG/'
                    if not os.path.isdir(path_jpg):
                        os.mkdir(path_jpg)
                    contador_jpg = 1
                shutil.move(path, path_jpg + file)
            if file.endswith(('gpr','GPR','raf','RAF')):
                if contador_raw == 0:
                    path_raw = nueva_carpeta + 'RAW/'
                    if not os.path.isdir(path_raw):
                        os.mkdir(path_raw)
                    contador_raw = 1
                shutil.move(path, path_raw + file)
    orden_secuencia(nueva_carpeta)
        
        
def orden_secuencia(nueva_carpeta):
    if os.path.isdir(nueva_carpeta + 'JPG/'):
        lista_fecha=[]
        nueva_secuencia = nueva_carpeta + 'JPG/'
        cuales = os.listdir(nueva_secuencia)
        cuantos = len(cuales)
        for z in range(cuantos):
            fecha = os.path.getmtime(nueva_secuencia + cuales[z])
            lista_fecha.append(fecha)
        lista_fecha.sort()
        contador = 1
        for y in range(cuantos):
            fecha_buscada = lista_fecha[y]
            for D, sD, f in os.walk(nueva_secuencia):
                for file in f:
                    if not file.startswith(('Timelapse')):
                        path = os.path.join(nueva_secuencia + file)
                        fecha_posible = os.path.getmtime(path)
                        if fecha_buscada == fecha_posible:
                            carpeta, archivo = os.path.split(path)
                            string_contador = str(contador)
                            secuencia_contador = string_contador.zfill(4)
                            secuencia_total = 'Timelapse_' + secuencia_contador + "_" + archivo
                            os.rename(path, nueva_secuencia + secuencia_total)
                            contador += 1
                            GPIO.output(led_pin, True)            
    if os.path.isdir(nueva_carpeta + 'RAW/'):
        lista_fecha=[]
        nueva_secuencia = nueva_carpeta + 'RAW/'
        cuales = os.listdir(nueva_secuencia)
        cuantos = len(cuales)
        for z in range(cuantos):
            fecha = os.path.getmtime(nueva_secuencia + cuales[z])
            lista_fecha.append(fecha)
        lista_fecha.sort()
        contador = 1
        for y in range(cuantos):
            fecha_buscada = lista_fecha[y]
            for D, sD, f in os.walk(nueva_secuencia):
                for file in f:
                    if not file.startswith(('Timelapse')):
                        path = os.path.join(nueva_secuencia + file)
                        fecha_posible = os.path.getmtime(path)
                        if fecha_buscada == fecha_posible:
                            carpeta,archivo = os.path.split(path)
                            string_contador = str(contador)
                            secuencia_contador = string_contador.zfill(4)
                            secuencia_total = 'Timelapse_' + secuencia_contador + "_" + archivo
                            os.rename(path, nueva_secuencia + secuencia_total)
                            contador += 1
                            GPIO.output(led_pin, True)
    print("secuencia lista")


def revision_duplicado_carpeta_destino_base(origen_file, file, carpeta_a_revisar):
    for d, sd, f in os.walk(carpeta_a_revisar):
        for archivo in f:
            archi,exten = os.path.splitext(file)
            if archi in archivo and archivo.endswith(exten):
                path = os.path.join(carpeta_a_revisar, d, archivo)
                size_archivo = os.path.getsize(path)
                size_file = os.path.getsize(origen_file)
                if size_archivo == size_file:
                    dup = 2
                    return dup       
    dup = 0
    return dup


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
    os.system(command_2)
    print('\n' + "End (Disk unmounted!)")

def start_pitimelapse():
    print("*** PiTimelapse ***" + '\n')
    path_source_disk, path_destination_disk = check_connected_disks()
    copy_timelapse_sd_to_ssd(path_source_disk, path_destination_disk)
    finalize(path_source_disk, path_destination_disk)


####################################### PiTimelapse #######################################
start_pitimelapse()