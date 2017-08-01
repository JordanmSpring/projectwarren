#!/bin/bash

array=( Xvfb geckodriver /usr/bin/firefox firefox /opt/google/chrome/chrome /opt/google/chrome/google-chrome chromedriver)
for i in "${array[@]}"
do
    for j in $(pgrep -f $i)
    do
        TIME=$(ps --no-headers -o etimes $j)
        if [ "$TIME" -ge $((60*30)) ] ; then
            echo $i,$j
            kill $j
        fi
    done
done
