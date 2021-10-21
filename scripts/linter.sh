#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit

# exit when any command fails
set -e

# run pylint on app
pylint --max-line-length=120 --disable=duplicate-code ./fab
