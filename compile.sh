#!/bin/bash
cd ROOT/static
while :
do
	scss style.scss > style.css
    coffee -c map.coffee
	coffee -c loading.coffee
	echo "Press [CTRL+C] to stop.."
	sleep 1
done
