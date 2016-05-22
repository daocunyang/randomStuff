#!/bin/sh

echo "" > ./info.txt
for i in 127.0.0.1;  # replace with your IP addresses
do
  ssh root@$i "hostname" >> ./info.txt
  ssh root@$i "/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'" >> ./info.txt
  ssh root@$i "grep -c ^processor /proc/cpuinfo" >> ./info.txt
  ssh root@$i "free -m | grep Mem | cut -c14-18" >> ./info.txt
  echo " " >> ./info.txt
  ssh root@$i "df -h | awk 'FNR==4{print $2}' " >> ./info.txt
  echo " " >> ./info.txt
  ssh root@$i "ps -ef | grep java" >> ./info.txt
  echo "" >> ./info.txt
  echo "--------------------------------------------------" >> ./info.txt
done
