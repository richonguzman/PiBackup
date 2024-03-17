#!/usr/bin/env python3

#----------------------------------------------------------#
#                     == PiBackup ==                       #
#                                                          #
#  A complete pack of great python scripts to Backup files #
#  with your Raspberry Pi 4:                               #
# - Backup your Camera SD-Card into your external SSD/HD   #
# - Clone your Backup SSD into another SSD                 #
# - Delete only JPG of your Backup SSD and keep RAW files  #
# - Analyze and Delete (optional) all duplicated files     #
# - Sort/Rename Timelapse files for importing ease         #
#                                                          #
#       https://github.com/richonguzman/PiBackup           #
#                                                          #
# Copyright (C) 2022 Ricardo Guzman richonguzman@gmail.com #
#                                                          #
#----------------------------------------------------------#



from flask import Flask, render_template, request, redirect
from hashlib import blake2s
from datetime import datetime
import RPi.GPIO as GPIO
import exiftool, os, shutil, subprocess, sys, time, glob

led_pin = 16               # 3mm Red LED in series with 2k2 resistor connected to pin 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setwarnings(False)

app = Flask(__name__)
        
def shut_down():
    time.sleep(5)
    os.system('sudo shutdown -h now')


@app.route("/", methods=['GET', 'POST'])
def welcome_home():
    templateData = {      'title' : 'Richon -',      }
    print("Home")
    GPIO.output(16, True)
    if request.method == 'POST':
        if request.form.get('Turn RP OFF') == 'Turn RP OFF':
            print("Turning RP OFF...")
            shut_down()
    return render_template('home.html', **templateData)
    
def generate_backup_output(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in iter(process.stdout.readline, ''):
        yield f"data: {line}\n\n"

@app.route('/pibackup_stream')
def pibackup_stream():
    command = [sys.executable, '/home/pi/PiBackup/pibackup.py', 's']
    return Response(generate_backup_output(command), mimetype='text/event-stream')

@app.route('/check_disks')
def check_disks():
    source_disk, destination_disk = check_connected_disks()
    return f"Source Disk: {source_disk}\nBackup Disk: {destination_disk}"

@app.route('/list_files_to_copy')
def list_files_to_copy_route():
    # You'll need to define the paths appropriately
    files_to_copy = list_files_to_copy(source_path, destination_path)
    files_to_copy_str = "<br>".join([f"{file['name']} - {file['extension']} - {file['date_modified']}" for file in files_to_copy])
    return files_to_copy_str

@app.route("/pibackup/", methods=['GET', 'POST'])
def pi_backup():
    templateData = {      'title' : 'Richon -',      }
    print("PiBackup")
    if request.method == 'POST':
        if request.form.get('PBK_J') == 'JPG':
            print("Pibackup only JPG")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pibackup.py','j'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('PBK_R') == 'RAW':
            print("Pibackup only RAW")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pibackup.py','r'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('PBK_JR') == 'JPG+RAW':
            print("Pibackup JPG + RAW")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pibackup.py','jr'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('PBK_V') == 'Video':
            print("Pibackup Video")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pibackup.py','v'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('PBK_JRV') == 'JPG+RAW+Video':
            print("Pibackup JPG + RAW + Video")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pibackup.py','jrv'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        return redirect('/pibackup_report/')
    return render_template('pibackup.html', **templateData)


@app.route("/piclone/", methods=['GET', 'POST'])
def pi_clone():
    templateData = {      'title' : 'Richon -',      }
    print("PiClone")
    if request.method == 'POST':
        if request.form.get('CLONE_BK') == "Clone 'PiBackup' folder":
            print("Clone PiBackup")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piclone.py','bk'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('CLONE_TM') == "Clone 'PiTimelapse' folder":
            print("Clone PiTimelapse")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piclone.py', 'tm'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('CLONE_BKTM') == "Clone 'PiBackup' and 'PiTimelapse'":
            print("Clone PiBackup and PiTimelapse")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piclone.py', 'bktm'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        return redirect('/pibackup_report/')
    return render_template('piclone.html', **templateData)


@app.route("/piclean/", methods=['GET', 'POST'])
def pi_clean():
    templateData = {      'title' : 'Richon -',      }
    print("PiClean")
    if request.method == 'POST':
        if request.form.get('CLEAN_BK') == "Clean 'PiBackup' folder":
            print("Clean PiBackup")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piclean.py','bk'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('CLEAN_TM') == "Clean 'PiTimelapse' folder":
            print("Clean PiTimelapse")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piclean.py', 'tm'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('CLEAN_BKTM') == "Clean 'PiBackup' and 'PiTimelapse'":
            print("Clean PiBackup and PiTimelapse")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piclean.py', 'bktm'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        return redirect('/pibackup_report/')
    return render_template('piclean.html', **templateData)


@app.route("/pitimelapse/", methods=['GET', 'POST'])
def pi_timelapse():
    templateData = {      'title' : 'Richon -',      }
    print("PiTimelapse")
    if request.method == 'POST':
        if request.form.get('T_J') == 'Timelapse JPG':
            print("Timelapse only JPG")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pitimelapse.py','j'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('T_R') == 'Timelapse RAW':
            print("Timelapse only RAW")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pitimelapse.py','r'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('T_JR') == 'Timelapse JPG+RAW':
            print("Timelapse JPG and RAW")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/pitimelapse.py','jr'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        return redirect('/pibackup_report/')
    return render_template('pitimelapse.html', **templateData)


@app.route("/piduplicated/", methods=['GET', 'POST'])
def pi_duplicated():
    templateData = {      'title' : 'Richon -',      }
    print("PiDuplicated")
    if request.method == 'POST':
        if request.form.get('DUP_LOG_JR') == "Duplicated JPG+RAW --> Log":
            print("Create LOG of Duplicated JPG+RAW Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py','log','jr'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('DUP_LOG_J') == "Duplicated JPG --> Log":
            print("Create LOG of Duplicated JPG Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py','log','j'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('DUP_LOG_R') == "Duplicated RAW --> Log":
            print("Create LOG of Duplicated RAW Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py','log','r'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('DUP_LOG_JRV') == "Duplicated JPG+RAW+VIDEO --> Log":
            print("Create LOG of Duplicated JPG+RAW+VIDEO Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py','log','jrv'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
            
        elif request.form.get('DUP_DELETE_JR') == "DELETE Duplicated JPG+RAW":
            print("Delete Duplicated JPG+RAW Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py', 'delete','jr'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('DUP_DELETE_J') == "DELETE Duplicated JPG":
            print("Delete Duplicated JPG Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py', 'delete','j'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('DUP_DELETE_R') == "DELETE Duplicated RAW":
            print("Delete Duplicated RAW Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py', 'delete','r'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        elif request.form.get('DUP_DELETE_JRV') == "DELETE Duplicated JPG+RAW+VIDEO":
            print("Delete Duplicated JPG+RAW+VIDEO Files")
            with open('/home/pi/PiBackup/report.log', 'wb') as f:
                process = subprocess.Popen([sys.executable, '/home/pi/PiBackup/piduplicated.py', 'delete','jrv'], stdout = subprocess.PIPE)
                for line in process.stdout:
#                     sys.stdout.write(str(line) + '\n')
                    f.write(line)
            f.close()
        return redirect('/pibackup_report/')
    return render_template('piduplicated.html', **templateData)


@app.route("/pibackup_report/")
def pi_report():
    templateData = {      'title' : 'Richon -',      }
    print("Finished Process")
    report = open('/home/pi/PiBackup/report.log','r')
    muestra = report.read()
    report.close
    return render_template('pibackup_report.html', **templateData, n = muestra )


if __name__ == "__main__":
    app.run(host= '192.168.100.1', port=5000, debug=True)