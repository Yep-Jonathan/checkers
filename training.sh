#!/bin/bash

for (( c=1; c<=50; c++ ))
do
  echo "$c"
  python checkers.py ai_vs_ai >>output 2>&1
done
