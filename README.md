# PiBackup

Transform your Raspberry Pi 4 (tested on RP 4 only) into your Photography companion like a Gnarbox (which currently is no more available as it seems the don't produce it anymore)

This will transform your Raspberry into an Wifi-Hotspot (with your custom SSID and Password if you like). Then you use your iPhone (soon the be tested with other brands) to connect to the Hotspot and open '192.168.100.1:5000/' and control the operations of the Backup in the webpage. You choose if you want only '.JPG' or only '.RAW' or just 'Video' files in the Backup.

-------------------------
NEW FUNTIONS:
1) PiBackup from SD to SSD:
- Connect the Backup Disk (to which the backup will be saved).
- Connect the Source Disk (usually a microSD/SD from your loved Camera).
- Checks/creates a 'PiBackup' folder on the Backup Disk (all backups will be saved inside this folder).
- By default it only copies files avoiding duplication (checking by name, size and even hash).
- Each file is processed to extract exif info and put each inside its own folder (Example: [FUJIFILM XT-3]).
- Each folder is then separated by '.JPG' or '.RAW' files into [JGP] and [RAW] folders to ease the uploading to your prefered photography editor.

2) PiClean: (Deletes only JPG Files from 'PiBackup' and/or 'PiTimelapse' folders to get more space if Backup-Disk is (almost) full)
- Connect the Backup Disk and let it work.

3) PiClone: (Clones 'PiBackup' and/or 'PiTimelapse' folders from Backup-Disk to another)
- Connect the New Backup Disk (to which the new backup will be cloned).
- Connect the Source Disk (your Backup-Disk) and let it work.

4) PiDuplicated: (Checks all your files in your Backup-Disk with hash info and makes a Log file of it or Deletes all duplicated files)
- Connect the Backup Disk and let it work.

5) PiTimelapse: (Backups all photographs from microSD/SD and sort/rename files into  for importing ease)
- Connect the Backup Disk (to which the backup will be saved).
- Connect the Source Disk (usually a microSD/SD from your loved Camera).
- Checks/creates a 'PiTimelapse' folder on the Backup Disk (all Timelapse Backups will be saved inside this folder).
- By default it only copies files avoiding duplication.
- Creates a folder with the oldes file date and the Camera Maker and Camera Model.
- Puts all photographs inside, separated by extension and renames each into 'Timelapse_000X'.

-------------------------

To start the 'PiBackup':
- "Burn" your microSD with Raspberry Pi OS Bullseye (the regular 32 bits version -not light-) [ 8GB microSD is enough ]
- Let it boot and set your Country, Languague and Timezone, Raspberry Pi OS Password, select your Wifi and Password and 'Next' for updates)
- Open a Terminal Window and write:
 
git clone https://github.com/richonguzman/PiBackup.git

cd PiBackup

bash install.sh


This will open a configuration program to select your :
- 'country_code' (two letters only, example: 'CL' (for Chile))
- 'WIFI-SSID'
- 'WIFI-Password'

let it install everything and it will reboot and will be ready to work (connect to the WIFI-SSID and open '192.168.100.1:5000/' for the menu)

-------------------------

Please help me get a new lens with:
--

[![Donate with PayPal](https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=GT9Z466ZSEFRN)
-------------------------

More things to come with this:
- any ideas to work with???
- anything we can think off
