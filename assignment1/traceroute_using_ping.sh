#!/bin/bash

MAX_HOPS=30

for (( ttl = 1; ttl <= $MAX_HOPS; ttl++ ))
do
	echo "========= Hop $ttl ============"
	ping -c 1 -t $ttl $1
done