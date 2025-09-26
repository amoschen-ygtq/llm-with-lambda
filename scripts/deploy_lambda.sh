#!/bin/bash

# The 'set -e' command instructs the shell to immediately exit if any command within the script returns a non-zero exit status.
# This helps prevent the script from continuing execution after an error, which can improve reliability and safety.
set -e

SRC_PATH="src"
BUILD_PATH=".build"
HANDLER_FILE="lambda_function.py"
SERVICES_PACKAGE_INIT="services/__init__.py"
BEDROCK_SERVICE_FILE="services/bedrock_chat_service.py"
SCRAPER_SERVICE_FILE="services/web_scraper_service.py"
PROMPT_SERVICE_FILE="services/prompt_service.py"
MODELS_PACKAGE="models"

LAMBDA_NAME="llm-with-lambda"
ZIP_FILE="lambda_package.zip"
ZIP_PATH="$BUILD_PATH/$ZIP_FILE"

# Create .build directory if it doesn't exist
rm -rf ".build/$LAMBDA_NAME"
mkdir -p ".build/$LAMBDA_NAME/services"
mkdir -p ".build/$LAMBDA_NAME/models"

# Copy handler file to .build/llm-with-lambda/
cp "$SRC_PATH/$HANDLER_FILE" "$BUILD_PATH/$LAMBDA_NAME/$HANDLER_FILE"

# Copy services files to .build/llm-with-lambda/services/
cp "$SRC_PATH/$SERVICES_PACKAGE_INIT" "$BUILD_PATH/$LAMBDA_NAME/$SERVICES_PACKAGE_INIT"
cp "$SRC_PATH/$BEDROCK_SERVICE_FILE"  "$BUILD_PATH/$LAMBDA_NAME/$BEDROCK_SERVICE_FILE"
cp "$SRC_PATH/$SCRAPER_SERVICE_FILE"  "$BUILD_PATH/$LAMBDA_NAME/$SCRAPER_SERVICE_FILE"
cp "$SRC_PATH/$PROMPT_SERVICE_FILE"  "$BUILD_PATH/$LAMBDA_NAME/$PROMPT_SERVICE_FILE"

# Copy models directory to .build/llm-with-lambda/models/
cp -r "$SRC_PATH/$MODELS_PACKAGE" "$BUILD_PATH/$LAMBDA_NAME"

# Export requirements.txt to .build/$LAMBDA_NAME/ from Pipfile in project root
pipenv requirements > "$BUILD_PATH/$LAMBDA_NAME/requirements.txt"

# Install dependencies into .build/$LAMBDA_NAME/ as individual folders
pip3 install --target "$BUILD_PATH/$LAMBDA_NAME/" -r "$BUILD_PATH/$LAMBDA_NAME/requirements.txt"

# Remove requirements.txt from .build/$LAMBDA_NAME/
rm "$BUILD_PATH/$LAMBDA_NAME/requirements.txt"

# Remove old zip if exists
rm -f "$ZIP_PATH"

# Create zip package
(cd ".build/$LAMBDA_NAME" && zip -r "../$ZIP_FILE" .)

# Deploy to AWS Lambda
aws lambda update-function-code \
    --function-name "$LAMBDA_NAME" \
    --zip-file "fileb://$ZIP_PATH" \
    --region us-east-1