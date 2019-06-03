#!/usr/bin/env bash
export COMPOSE_PROJECT_NAME=ford3
export COMPOSE_FILE=docker-compose.yml$(if [ -f docker-compose.override.yml ]; then echo ":docker-compose.override.yml"; fi):scripts/travis/selenium-compose.yml
export ANSIBLE_PROJECT_SETUP_DIR=ansible
