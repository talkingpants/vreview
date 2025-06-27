#!/usr/bin/env bash
# Install Python dependencies needed for running the test suite.
# Usage: ./setup_tests.sh

set -e

# Install backend requirements
pip install -r backend/requirements.txt

# Ensure pytest is available
pip install pytest

# Indicate success
echo "Dependencies installed. You can now run \`pytest\`."
