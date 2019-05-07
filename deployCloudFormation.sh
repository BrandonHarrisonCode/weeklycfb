
# Not sure if setting this is necessary. TravisCI might do this be default.
set -e

# This sets up environment variables for the rest of the build/deploy cycle.
# If master is being pushed, then everything needs to be set to production.
# Otherwise, the deployment stage is development and the stack and folder have the branch name prepended.
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

# Check the aws-cli and aws-sam-cli versions in case something breaks
aws --version
sam --version

# Follow the CloudFormation deploy steps using aws-sam-cli and aws-cli
sam validate
sam build --use-container
sam package --output-template-file packaged.yml --s3-bucket cfb-game-of-the-week-zip-files
sam deploy --template-file packaged.yml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --region us-east-1 --parameter-overrides DeploymentStage=${DEPLOYMENT_STAGE}

# Update the scrips.js file to refer to the new URL:
# This file begins with a const declaration of the URL for the accessLambda.
# The URL is obtained by querying aws using describe-stacks and returning only the OutputValue.
# If there are more keys and values set to Output in our template, this strategy will have to change.
# The URL is piped to an empty tmpfile (should probably be made using random timestamp) as a const declaration,
# and then the entire frontEnd/script.js file is appended to this temp file, minus the first line of
# script.js. This tmpfile then replaces frontEnd/script.js.

echo "Updating script file..."
API_URL=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --query Stacks[].Outputs[*].[OutputValue] --output text)
echo "const lambdaURL = '${API_URL}'" > tmpfile
sed '1d' frontEnd/script.js >> tmpfile
rm frontEnd/script.js && mv tmpfile frontEnd/script.js
echo "The file script.js was updated."

# Output the new contents of script.js in case there are errors.
cat frontEnd/script.js

# Output info about the branch and the API URL.
echo This build was pushed from branch ${TRAVIS_BRANCH}.
echo The API URL is ${API_URL}