#!/bin/bash

for (( c=1; c<=1000; c++ ))
do
  echo "$c"
  python checkers.py training
done
