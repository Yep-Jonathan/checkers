#!/bin/bash

for (( c=1; c<=500; c++ ))
do
  echo "$c"
  python checkers.py training
done
