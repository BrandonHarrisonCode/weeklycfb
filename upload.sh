#!/bin/bash

set -e

sam validate
sam build
sam package --output-template-file packaged.yml --s3-bucket cfb-game-of-the-week-zip-files
sam deploy --template-file packaged.yml --stack-name CloudFormationVer3 --capabilities CAPABILITY_IAM --region us-east-1 --parameter-overrides DeploymentStage=Dev
