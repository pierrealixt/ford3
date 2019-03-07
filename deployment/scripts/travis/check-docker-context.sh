#!/usr/bin/env bash

# If PR contains changes to docker context, we need to check that
# the build works.

if git diff --exit-code HEAD...${TRAVIS_BRANCH} -- deployment/docker && git diff --exit-code HEAD..${TRAVIS_BRANCH} -- deployment/production; then
	# It means no change.
	# Use existing docker image with latest tag
	echo "No changes in Docker context. Use latest tag"
	cp deployment/scripts/travis/docker-compose.override.nobuild.yml deployment/docker-compose.override.yml
else
	echo "Changes detected in Docker context. Will attempt to test build"
	cp deployment/scripts/travis/docker-compose.override.newbuild.yml deployment/docker-compose.override.yml
fi
