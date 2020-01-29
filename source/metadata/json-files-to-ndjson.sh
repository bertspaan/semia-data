#!/usr/bin/env bash

for filename in $1/*.json; do
  jq -M -r -c '.' $filename  
done
