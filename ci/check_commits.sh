#!/bin/bash

# Pattern pour valider le message de commit
COMMIT_MSG_REGEX="^:?(feat|fix|docs|style|refactor|test|chore): ?.+"

commit_message="$1"

if ! echo "$commit_message" | grep -qE "$COMMIT_MSG_REGEX"; then
  echo "Error: The commit message does not follow conventions."
  echo "The message must begin with one of the following keywords: feat, fix, docs, style, refactor, test, chore."
  exit 1
fi