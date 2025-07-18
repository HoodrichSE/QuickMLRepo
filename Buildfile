#!/bin/bash
# Buildfile (place in root directory of your app)

# Create temporary directory with more space
mkdir -p /var/app/large_tmp
export TMPDIR=/var/app/large_tmp

# Install pip dependencies with custom temp directory
#pip install --upgrade pip
#pip install --no-cache-dir --tmp-dir /var/app/large_tmp tensorflow
#pip install --no-cache-dir --tmp-dir /var/app/large_tmp pandas numpy
#pip install --no-cache-dir --tmp-dir /var/app/large_tmp seaborn matplotlib scikit-learn
#pip install --no-cache-dir --tmp-dir /var/app/large_tmp catboost xgboost dill flask
pip install -r requirements.txt --tmp-dir /var/app/large_tmp

# Clean up
rm -rf /var/app/large_tmp