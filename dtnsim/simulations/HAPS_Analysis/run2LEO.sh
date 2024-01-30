#!/bin/bash

cd 2LEO_1GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_2GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_5GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_10GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_1HAP_1GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_2HAP_2GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_3HAP_3GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_4HAP_4GS
chmod +x script.sh
./script.sh &
cd ..

cd 2LEO_5HAP_5GS
chmod +x script.sh
./script.sh &
cd ..

wait