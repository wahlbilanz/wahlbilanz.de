#!/bin/bash

# neueste namentliche abstimmung
last=721
first=487
url_prefix="https://www.bundestag.de/parlament/plenum/abstimmung/abstimmung?id="


for i in $(seq ${first} ${last})
do
    if [ -f "$i" ]
    then
        echo "skipping $i"
    else
        echo "downloading $url_prefix$i"
        curl -s -q "$url_prefix$i" > "$i"
    fi
done


