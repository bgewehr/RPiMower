sudo python ./sonic_1.py &
sudo python ./groundCam.py &
sudo python ./RPiMower.py &

read -n1 -rsp "Press any key to continue... "
sudo killall python

