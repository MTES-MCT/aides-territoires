#!/bin/bash

# Ansible doesn't seem to have a lookup for .env files.
# This script is a wrapper around the ansbile command.
# It loads a dotenv file into environment variables and make them
# available to ansible.

ENV_FILE="$(dirname "$0")/src/.env.ansible"

set -o nounset -o pipefail -o errexit

# Load all variables from dotenv and export them all for Ansible to read
set -o allexport
source $ENV_FILE
set +o allexport

# Run Ansible
exec ansible-playbook "$@"