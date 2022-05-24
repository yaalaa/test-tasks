#!/bin/bash

# parameters
MY_FIRST_REV_IN=$1

# hard parameters
MY_VERSION_RE='^\*Version\s+[0-9]+\.[0-9]+(\.[0-9]+)?'
MY_ONLY_MASK='^\*'

# check it's git repo
_=$(git rev-parse --show-toplevel 2>&1)
if [ "$?" -ne "0" ]; then
  echo "Error: it is not git repo"
  exit 1
fi

# get current rev hash
MY_REV_HASH=$(git rev-parse HEAD^{} 2>&1)
if [ "$?" -ne "0" ]; then
  echo "Error: cannot get current revision"
  exit 1
fi

# what would be the first
if [[ "${MY_FIRST_REV_IN}" != "" ]]; then
  MY_FIRST_REV_HASH=$(git rev-parse --quiet --verify "${MY_FIRST_REV_IN}^{}")
  if [ "$?" -ne "0" ]; then
    echo "Error: bad commit hash - \"${MY_FIRST_REV_IN}\""
    exit 1
  fi
  if [[ "${MY_FIRST_REV_HASH}" == "" ]]; then
    echo "Error: bad input commit hash - \"${MY_FIRST_REV_IN}\""
    exit 1
  fi
else
  MY_FIRST_REV_HASH=${MY_REV_HASH}
fi

# look for version commits
MY_VERSION_REVS_OUT=($(git rev-list ${MY_FIRST_REV_HASH} --extended-regexp --grep=${MY_VERSION_RE} -n2 2>&1))
if [ "$?" -ne "0" ]; then
  echo "Error: cannot parse revisions"
  exit 1
fi
MY_FISRT_VERSION_REV=no
MY_NEXT_VERSION_REV=#
MY_IDX=0
for MY_VER in "${MY_VERSION_REVS_OUT[@]}"; do
  if [[ "${MY_VER}" == "" ]]; then
    break
  fi
  if [[ "${MY_IDX}" -eq 0 ]] && [[ "${MY_VER}" == "${MY_FIRST_REV_HASH}" ]]; then
    MY_FISRT_VERSION_REV=yes
    MY_IDX=$((MY_IDX + 1))
    continue
  fi
  MY_NEXT_VERSION_REV="${MY_VER}"
  break
done
if [[ "${MY_NEXT_VERSION_REV}" == "" ]]; then
  echo "Error: previous version commit was not found"
  exit 1
fi
#echo "First: \"${MY_NEXT_VERSION_REV}\""
#echo "Next: \"${MY_NEXT_VERSION_REV}\""

# get the log
if [[ "${MY_ONLY_MASK}" == "" ]]; then
  MY_ONLY_MASK='.'
fi

git log --format='%s' --extended-regexp --grep=${MY_ONLY_MASK} ${MY_NEXT_VERSION_REV}..${MY_FIRST_REV_HASH}

