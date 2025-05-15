#!/bin/bash


# ======================================
# 🚀 DEPLOY NAVI TO AWS LAMBDA
# ======================================

# ========= CONFIGURATION ==========
FUNCTION_NAME="Navi-Bot"
ZIP_FILE="assistant.zip"
VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"
BUILD_DIR="build"
SOURCE_FILES=("assistant.py" "memory.py")
# ==================================

# Clean previous build
echo "🧹 Cleaning previous build and zip..."
rm -f $ZIP_FILE
rm -rf $BUILD_DIR

# Create build directory
echo "📂 Creating build directory..."
mkdir -p $BUILD_DIR

# Install dependencies to build dir
echo "📦 Installing dependencies into build dir..."
pip install -r $REQUIREMENTS -t $BUILD_DIR || {
    echo "❌ Failed to install requirements. Exiting."
    exit 1
}

echo "📂 Copying source files..."
for file in "${SOURCE_FILES[@]}"; do
  cp "navi/$file" build/
done
#cp navi/assistant.py $BUILD_DIR/
#cp navi/memory.py $BUILD_DIR/


if [ -f ".env" ]; then
  echo "🧪 Including .env for local testing..."
  cp .env $BUILD_DIR/
fi

echo "🗜️ Zipping final build..."
cd $BUILD_DIR
zip -r ../$ZIP_FILE . -x '*.DS_Store' '*__pycache__*' '*.pyc'
cd ..

# Deploy to Lambda
echo "🚀 Uploading $ZIP_FILE to Lambda function: $FUNCTION_NAME"
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file "fileb://$ZIP_FILE"

echo "✅ Lambda deployment complete!"



