#! /bin/sh
# Autostart script for RaspiBrick

# set -x

echo "Running Process Monitor. Sleeping a while..."
sleep 10 # Wait until system is up and running
echo "Continuing..."

# copy wlan info from FAT partition and restart wlan
sudo mkdir /mnt/recovery
sudo mount /dev/mmcblk0p1 /mnt/recovery
cp /mnt/recovery/brickgate.data /home/pi/brickgate.data
sudo cp /mnt/recovery/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo ifdown wlan0
sudo ifup wlan0 

cd /home/pi/brickgate
python ProcessMon.py
