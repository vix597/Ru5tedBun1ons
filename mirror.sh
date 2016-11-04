#!/bin/bash

read -p "bridge> " BRIDGE 
read -p "src port (what you want to mirror)> " SRC_PORT
read -p "dest port (what port will it go to)> " DEST_PORT

ovs-vsctl -- set Bridge $BRIDGE mirrors=@m \
 -- --id=@src get Port $SRC_PORT \
 -- --id=@dest get Port $DEST_PORT \
 -- --id=@m create Mirror name=mymirror select-dst-port=@src select-src-port=@src output-port=@dest

