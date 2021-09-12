#!/bin/bash

set -ex

git init
git remote add origin https://github.com/mch2/OpenSearch.git
git fetch --depth 1 origin $1
git checkout FETCH_HEAD

./gradlew check --no-daemon --no-scan -x bwcTest

echo "GRADLE CHECK COMPLETED, RUNNING BWC"

./gradlew bwcTest