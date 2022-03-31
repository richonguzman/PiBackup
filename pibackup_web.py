#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
from hashlib import blake2s
from datetime import datetime
import RPi.GPIO as GPIO
import exiftool
import os
import shutil
import subprocess
import sys
import time
import glob


GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setwarnings(False)

app = Flask(__name__)
        
def apagado():
    time.sleep(5)
    os.system('sudo shutdown -h now')


@app.route("/", methods=['GET', 'POST'])
def bienvenida():
    templateData = {      'title' : 'Richon -',      }
    print("Home")
    if request.method == 'POST':
        if request.form.get('Turn RP OFF') == 'Turn RP OFF':
            print("Turning RP OFF...")
            apagado()
    return render_template('home.html', **templateData)
    
    
@app.route("/pibackup/", methods=['GET', 'POST'])
def pibk():
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

@app.route("/pibackup_report/")
def proceso_o():
    templateData = {      'title' : 'Richon -',      }
    print("Finished Process")
    report = open('/home/pi/PiBackup/report.log','r')
    muestra = report.read()
    report.close
    return render_template('pibackup_report.html', **templateData, n = muestra )


if __name__ == "__main__":
    app.run(host= '192.168.100.1', port=5000, debug=True)