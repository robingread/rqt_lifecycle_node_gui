#! /bin/bash

set -e

./scripts/build-test.sh
./scripts/test-rqt-plugin.sh
