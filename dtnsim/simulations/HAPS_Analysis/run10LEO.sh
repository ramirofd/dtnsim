#!/bin/bash

cd 10LEO_1GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_2GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_5GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_10GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_1HAP_1GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_2HAP_2GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_3HAP_3GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_4HAP_4GS
chmod +x script.sh
./script.sh &
cd ..

cd 10LEO_5HAP_5GS
chmod +x script.sh
./script.sh &
cd ..


wait