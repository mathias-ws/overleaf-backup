#!/bin/bash
# Credits to https://stackoverflow.com/a/68358639 for the switch case solution to this problem.
case "$1" in
    Username*) exec echo "$GIT_USERNAME" ;;
    Password*) exec echo "$GIT_PASSWORD" ;;
esac
