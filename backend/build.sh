#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python migrations.py

# Add any other build steps here
echo "Build completed successfully"