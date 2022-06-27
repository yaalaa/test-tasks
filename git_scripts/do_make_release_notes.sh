#!/bin/bash

# parameters
MY_FIRST_REV_IN=$1

# hard parameters
MY_VERSION_RE='^\*\s*Version\s+(=\s+)?[0-9]+\.[0-9]+(\.[0-9]+)?'
MY_VERSION_RE_CASE_SENSITIVE=no#yes
MY_ONLY_MASK='^\*'
MY_TICKET_MASK='[*[:space:]]([a-zA-Z]+-[0-9]+)[,[:space:]]'

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
if [[ "${MY_VERSION_RE_CASE_SENSITIVE}" == "yes" ]]; then
  MY_REVLIST_RE_CASE_SENSITIVE=""
else
  MY_REVLIST_RE_CASE_SENSITIVE=" --regexp-ignore-case"
fi
MY_VERSION_REVS_OUT=($(git rev-list ${MY_FIRST_REV_HASH}${MY_REVLIST_RE_CASE_SENSITIVE} --extended-regexp --grep=${MY_VERSION_RE} -n2 2>&1))
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

# get log
MY_LOG=$(git log --format='%s' --extended-regexp --grep=${MY_ONLY_MASK} ${MY_NEXT_VERSION_REV}..${MY_FIRST_REV_HASH} 2>&1)
if [ "$?" -ne "0" ]; then
  echo "Error: cannot git log"
  exit 1
fi

# get tickets
MY_TICKETS_TMP=()
MY_LOG_TMP="${MY_LOG}"
while [[ "${MY_LOG_TMP}" =~ ${MY_TICKET_MASK} ]]; do
  MY_TICKETS_TMP+=(${BASH_REMATCH[1]})
  MY_LOG_TMP=${MY_LOG_TMP/"${BASH_REMATCH[0]}"/ }
done
IFS=$'\n'; MY_TICKETS=($(sort -uV <<<"${MY_TICKETS_TMP[*]}")); unset IFS
if [[ "${#MY_TICKETS[@]}" -gt 1 ]]; then
  MY_TICKETS_LIST="${MY_TICKETS[0]}$(printf ", %s" "${MY_TICKETS[@]:1}")"
else
  MY_TICKETS_LIST="${MY_TICKETS[*]}"
fi
if [[ "${#MY_TICKETS[@]}" -gt 0 ]]; then
  printf "Tickets\n----\n${MY_TICKETS_LIST}\n\nTL;DR\n----\n"
fi

# dump log
echo "${MY_LOG}"
