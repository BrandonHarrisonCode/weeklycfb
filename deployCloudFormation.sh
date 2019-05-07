if [ $TRAVIS_BRANCH -eq "master" ] then
  STACKNAME="ProductionStack"
  DEPLOYMENTSTAGE="Production"
else
  STACKNAME="${TRAVIS_BRANCH}Stack"
  DEPLOYMENTSTAGE="Dev"
fi

aws --version
sam --version
sam validate
sam build --use-container
sam package --output-template-file packaged.yml --s3-bucket cfb-game-of-the-week-zip-files
sam deploy --template-file packaged.yml --stack-name $STACKNAME --capabilities CAPABILITY_IAM --region us-east-1 --parameter-overrides DeploymentStage=$DEPLOYMENTSTAGE

echo "Updating script file..."
APIURL=$(aws cloudformation describe-stacks --stack-name $STACKNAME --query Stacks[].Outputs[*].[OutputValue] --output text)
echo "const lambdaURL = '$APIURL'" > tmpfile
sed '1d' frontEnd/script.js >> tmpfile
rm frontEnd/script.js && mv tmpfile frontEnd/script.js
echo "The file script.js was updated."
cat frontEnd/script.js
echo "SUCCESS"
echo This build was pushed from branch ${TRAVIS_BRANCH}.
echo The API URL is $APIURL