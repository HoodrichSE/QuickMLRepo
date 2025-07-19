#!/bin/bash
set -o pipefail
set -x

printf "Creating temporary dir and cache for pip..."
mkdir -p /var/app/pip_temp && chmod 777 /var/app/pip_temp
mkdir -p /var/app/pip_cache && chmod 777 /var/app/pip_cache