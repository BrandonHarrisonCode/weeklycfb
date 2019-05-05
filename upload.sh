#!/usr/bin/bash

set -e

lambda_folder_suffix=Module
lambdas=$(find . -maxdepth 1 -name "*${lambda_folder_suffix}" -print)
for folder in ${lambdas}
do
    basename=$(basename ${folder})
    cd ${basename}
    cd venv/lib/python3.7/site-packages/
    zip -r9 ../../../../function.zip .
    cd ../../../../
    zip -g function.zip *.py
    aws s3 --profile cfb cp function.zip s3://cfb-game-of-the-week-zip-files/function-${basename}.zip
    cd ..
done
