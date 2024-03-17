#!/bin/bash

# Function to backup a file before it's replaced
backup_file() {
    local file=$1
    local backup_file="${file}.backup"
    if [ -f "$file" ]; then
        echo "Backing up $file to $backup_file"
        sudo cp $file $backup_file
    fi
}

# Exit script on error
set -e

# Enable script tracing
set -x

echo "Running config.py"
python3 /home/pi/PiBackup/conf/config.py
sleep 1

echo "Updating profile with update_profile.py"
python3 /home/pi/PiBackup/conf/update_profile.py
sleep 3

echo "Updating package lists"
sudo apt update
sleep 1

echo "Installing required packages"
sudo apt install exfat-fuse exfat-utils ntfs-3g -y
sleep 1

sudo apt-get install -y libimage-exiftool-perl
sleep 1

sudo pip3 install PyExifTool 
sleep 1

sudo apt install hostapd dnsmasq -y
sleep 1

echo "Unmasking and enabling hostapd"
sudo systemctl unmask hostapd
sleep 1

sudo systemctl enable hostapd
sleep 1

sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
sleep 1

backup_file "/etc/dhcpcd.conf"
echo "Replacing dhcpcd.conf"
sudo cp /home/pi/PiBackup/conf/PBK_dhcpcd.conf /etc/dhcpcd.conf
sleep 1

backup_file "/etc/sysctl.d/routed-ap.conf"
echo "Replacing routed-ap.conf"
sudo cp /home/pi/PiBackup/conf/PBK_routed-ap.conf /etc/sysctl.d/routed-ap.conf
sleep 1

echo "Setting up IP forwarding"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sleep 1

sudo netfilter-persistent save
sleep 1

backup_file "/etc/dnsmasq.conf"
echo "Replacing dnsmasq.conf"
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo cp /home/pi/PiBackup/conf/PBK_dnsmasq.conf /etc/dnsmasq.conf
sleep 1

echo "Unblocking WLAN"
sudo rfkill unblock wlan
sleep 1

backup_file "/etc/hostapd/hostapd.conf"
echo "Replacing hostapd.conf"
sudo cp /home/pi/PiBackup/conf/PBK_hostapd.conf /etc/hostapd/hostapd.conf
sleep 1

backup_file "/etc/profile"
echo "Replacing profile file"
sudo cp /home/pi/PiBackup/conf/profile /etc/profile
sleep 5

echo "Rebooting system"
sudo systemctl reboot
