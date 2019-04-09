#!/bin/sh

for i in $(\grep username /tmp/eu-deputies.json | sed 's/^.*: "\([^"]*\)".*$/\1/g')
do
    echo $i
    curl -s https://www.abgeordnetenwatch.de/api/parliament/eu-parlament%202014-2019/profile/$i/profile.json | python -mjson.tool > abgeordnetenwatch-individual-votes/$i.json
done
