set -e

if [ $TRAVIS_BRANCH -eq "master" ]
then
  STACK_NAME="ProductionStack"
  DEPLOYMENT_STAGE="Production"
  FOLDER_NAME="ProductionWebResources"
else
  STACK_NAME="${TRAVIS_BRANCH}Stack"
  DEPLOYMENT_STAGE="Dev"
  FOLDER_NAME="${TRAVIS_BRANCH}WebResources"
fi

aws --version
sam --version
sam validate
sam build --use-container
sam package --output-template-file packaged.yml --s3-bucket cfb-game-of-the-week-zip-files
sam deploy --template-file packaged.yml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --region us-east-1 --parameter-overrides DeploymentStage=${DEPLOYMENT_STAGE}

echo "Updating script file..."
API_URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query Stacks[].Outputs[*].[OutputValue] --output text)
echo "const lambdaURL = '${API_URL}'" > tmpfile
sed '1d' frontEnd/script.js >> tmpfile
rm frontEnd/script.js && mv tmpfile frontEnd/script.js
echo "The file script.js was updated."
cat frontEnd/script.js
echo "SUCCESS"
echo This build was pushed from branch ${TRAVIS_BRANCH}.
echo The API URL is ${API_URL}