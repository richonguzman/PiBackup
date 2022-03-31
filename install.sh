python3 /home/pi/PiBackup/conf/config.py
sleep 3
sudo apt update
sleep 1
sudo apt install exfat-fuse exfat-utils ntfs-3g -y
sleep 1
sudo apt-get install -y libimage-exiftool-perl
sleep 1
sudo pip3 install PyExifTool 
sleep 1
sudo apt install hostapd dnsmasq -y
sleep 1
sudo systemctl unmask hostapd
sleep 1
sudo systemctl enable hostapd
sleep 1
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
sleep 1
sudo cp /home/pi/PiBackup/conf/PBK_dhcpcd.conf /etc/dhcpcd.conf
sleep 1
sudo cp /home/pi/PiBackup/conf/PBK_routed-ap.conf /etc/sysctl.d/routed-ap.conf
sleep 1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sleep 1
sudo netfilter-persistent save
sleep 1
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sleep 1
sudo cp /home/pi/PiBackup/conf/PBK_dnsmasq.conf /etc/dnsmasq.conf
sleep 1
sudo rfkill unblock wlan
sleep 1
sudo cp /home/pi/PiBackup/conf/PBK_hostapd.conf /etc/hostapd/hostapd.conf
sleep 5
sudo systemctl reboot