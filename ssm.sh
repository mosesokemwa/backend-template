#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <parameterDir>"
  exit 1
fi

parameterDir=$1

aws ssm get-parameters-by-path --with-decryption --path $parameterDir --recursive --query "Parameters[*].{Name:Name,Value:Value}" | \
  jq -r '.[] | "\(.Name | split("/") | last)=\"\(.Value)\""' > env.tmp

mv env.tmp .env
