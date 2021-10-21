#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit

bandit -r ./fab
