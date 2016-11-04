#!/bin/bash

read -p "bridge> " BRIDGE 

ovs-vsctl clear Bridge $BRIDGE mirrors

