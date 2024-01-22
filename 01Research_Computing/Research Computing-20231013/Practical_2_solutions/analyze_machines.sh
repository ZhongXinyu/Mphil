#!/bin/bash

for m in $*; do
    procs=`ssh $m cat /proc/cpuinfo | grep processor | wc -l`
    ram=`ssh $m free -m | awk '/Mem/{print $2;}'`
    users=`ssh $m who | awk '{print $1;}' | sort | uniq | wc -l`
    recent_users=`ssh $m last | awk '{print $1;}' | sort | uniq | wc -l`    
    load=`ssh $m cat /proc/loadavg | awk '{print $3;}'`
    
    echo "========== $m ==========="
    echo "Has $procs cores and ${ram}MB of memory."
    echo "There are currently $users users, and $recent_users recent users"
    echo "The 15min load-average is $load."
done
