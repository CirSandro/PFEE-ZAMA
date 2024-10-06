#!/bin/bash

# Commit message pattern
COMMIT_MSG_REGEX="^ ?(feat|fix|docs|style|refactor|test|chore): .+"

commit_message="$1"

if ! echo "$commit_message" | grep -qE "$COMMIT_MSG_REGEX"; then
  echo "Error: The commit message does not follow conventions."
  echo "The message must begin with one of the following regex: ^ ?(feat|fix|docs|style|refactor|test|chore): .+"
  exit 1
fi

# Verify commit length
if [ ${#commit_message} -gt 50 ]; then
  echo "Error: The commit message exceeds 50 characters."
  echo "Current length: ${#commit_message}. The maximum allowed is 50 characters."
  exit 1
fi 