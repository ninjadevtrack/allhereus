#!/usr/bin/env bash

if [[ "$1" == "y" ]]; then
  silent_mode=$1
else
  silent_mode=""
fi

if [[ ! ${silent_mode} == "y" ]]; then
  echo "Here's all the old SDK directories"
  ls -d ednudge-sdk-python_*

  read -p "Are you sure you want to delete the old SDK directories? (Anything other than y aborts) " -n 1 -r
  if [[ ! ${REPLY} == "y" ]]; then
    echo ""
    echo "Aborting."
    exit 0
  fi

  echo "Deleting all the old SDK directories"
fi

rm -rf ednudge-sdk-python_*
