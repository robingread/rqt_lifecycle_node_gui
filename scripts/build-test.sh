#! /bin/bash

set -e

# Set up paths
COVERAGE_DIR=coverage
LCOV_FILE=${COVERAGE_DIR}/coverage.info
HTML_DIR=${COVERAGE_DIR}/html

export QT_QPA_PLATFORM=offscreen

# Clean and rebuild the project
colcon clean workspace --yes
colcon build \
    --cmake-args \
        -DCMAKE_BUILD_TYPE=Debug \
        -DCMAKE_CXX_FLAGS="--coverage" \
        -DCMAKE_C_FLAGS="--coverage"

# Run tests
colcon test
colcon test-result --verbose --all

# Create coverage directory
mkdir -p ${COVERAGE_DIR}

# Run fastcov to generate coverage.json
python3 -m fastcov \
    -d . \
    --include src/ \
    --exclude /usr/include \
    --exclude /opt/ros \
    --exclude "**/test/*" \
    --lcov \
    --output ${COVERAGE_DIR}/coverage.info

# Generate HTML report with genhtml
genhtml ${COVERAGE_DIR}/coverage.info -o ${HTML_DIR}

echo "Coverage report generated at ${HTML_DIR}/index.html"
