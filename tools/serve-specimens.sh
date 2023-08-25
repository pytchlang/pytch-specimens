#!/bin/bash

set -e

########################################################################

have_all_tools=yes
for tool in realpath poetry; do
    if ! hash "$tool" 2> /dev/null; then
        echo Could not find "$tool"
        have_all_tools=no
    fi
done

if [ "$have_all_tools" = "no" ]; then
    echo
    echo "Required tool/s missing.  Please install it/them and try again."
    exit 1
fi

########################################################################

TOOLS_DIR="$(realpath "$(dirname "$0")")"

cd "$TOOLS_DIR"

n_poetry_envs=$(poetry env list | wc -l)
if [ "$n_poetry_envs" = "0" ]; then
    poetry install
fi

poetry run python serve_bundle.py "$@"
