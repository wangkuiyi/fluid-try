#!/bin/bash
set -e

readonly VERSION="version 7."

version=$(clang-format -version)

if ! [[ $version == *"$VERSION"* ]]; then
    echo "clang-format version check failed."
    echo "a version contains '$VERSION' is needed, but get '$version'"
    echo "you can install the right version, and make an soft-link to '\$PATH' env"
    exit -1
fi

clang-format $@
