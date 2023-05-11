#!/bin/bash

if [ -f .env.local ]; then
  export $(echo $(cat .env.local | sed 's/#.*//g'| xargs) | envsubst)
fi

echo "Downloading file from $GRAND_EST_FILE_PATH"
wget --inet4-only -P /tmp/ $GRAND_EST_FILE_PATH
