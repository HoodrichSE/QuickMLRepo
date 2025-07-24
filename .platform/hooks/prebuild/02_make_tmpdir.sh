#!/bin/bash
set -o
set -e


printf "Creating temporary dir and cache for pip..."
mkdir -p /var/app/pip_temp && chmod 777 /var/app/pip_temp
mkdir -p /var/app/pip_cache && chmod 777 /var/app/pip_cache
export TMPDIR=/var/app/pip_temp #Could also use /var/tmp
printf "$TMPDIR"
python3.12 -m pip config set global.cache-dir "/var/app/pip_cache"