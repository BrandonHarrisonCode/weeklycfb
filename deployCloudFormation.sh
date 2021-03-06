
# Not sure if setting this is necessary. TravisCI might do this be default.
set -e

# This sets up environment variables for the rest of the build/deploy cycle.
# If master is being pushed, then everything needs to be set to production.
# Otherwise, the deployment stage is development and the stack and folder have the branch name prepended.
STACK_NAME="ProductionStack"
DEPLOYMENT_STAGE="Production"
FOLDER_NAME="ProductionWebResources"
CLOUDFRONT_DISTRIBUTION_ID="E1BEVY7FP1UR6X"
S3_BUCKET="s3://cfbgameoftheweek.com"

# Check the version numbers in case something breaks
python --version
aws --version
sam --version
yarn --version

black --check .

sam validate
for folder in $(find . -type d -name \*Module) ; do 
  docker build --network host -t module ${folder}
  docker run --network host -e AWS_DEFAULT_REGION -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY module
done

yarn --cwd frontend install --ignore-engines
yarn --cwd frontend test
yarn --cwd frontend build
aws s3 sync frontend/build "${S3_BUCKET}"

# Follow the CloudFormation deploy steps using aws-sam-cli and aws-cli
sam build
sam package --output-template-file packaged.yml --s3-bucket cfb-game-of-the-week-zip-files
if [[ "${TRAVIS_BRANCH}" == "master" ]]
then
  sam deploy --template-file packaged.yml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --region us-east-1 --parameter-overrides DeploymentStage=${DEPLOYMENT_STAGE} --force-upload --no-fail-on-empty-changeset
fi


