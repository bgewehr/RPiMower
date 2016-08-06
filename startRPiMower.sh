sudo python ./sens_frontSonar.py &
sudo python ./sens_groundCam.py &
sudo python ./sens_imu.py &
sudo python ./sens_pcf8591t.py &
sudo python ./RPiMower.py &

read -n1 -rsp "Press any key to continue... "
sudo killall python

