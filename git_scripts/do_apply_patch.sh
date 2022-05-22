#!/bin/bash
# be sure to make it executable - like
#   chmod u+x do_apply_patch.sh
# then just go to repo folder and run this script

# parameters
MY_REMOTE_BRANCH=master
MY_LOCAL_BRANCH=feature-branch
MY_PATCH_DIR=/Users/<username>/Downloads/<patch_folder>

# debug parameters
#MY_DEBUG_REMOVE_LOCAL_BRANCH=master

# hard parameters
MY_PATCH_EXT=.diff

# colors
if tty -s; then
  _NC='\033[0m'
  _RC='\033[0;31m'
  _BC='\033[0;34m'
else
  _NC=
  _RC=
  _BC=
fi
S_ERR="${_RC}Error"

# thanks to
# https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# dump current path
echo -e "${_BC}Current directory: $(pwd)${_NC}"

# check patch directory exists
if [ "${MY_PATCH_DIR}" == "" ]; then
  if [ "${SCRIPTPATH}" == "" ]; then
    echo -e "${S_ERR}:patch directory is not specified${_NC}"
    exit 1
  fi
  # let's use SCRIPTPATH
  MY_PATCH_DIR=${SCRIPTPATH}
fi
if [ ! -d "${MY_PATCH_DIR}" ]; then
  echo -e "${S_ERR}: patch directory does not exist - ${MY_PATCH_DIR}${_NC}"
  exit 1
fi

# check there are patch files
MY_HAVE_PATCH_FILES=0
for filename in ${MY_PATCH_DIR}/*${MY_PATCH_EXT}; do
  if [ -f "${filename}" ]; then
    MY_HAVE_PATCH_FILES=1
    break
  fi
done
if [ "${MY_HAVE_PATCH_FILES}" -eq "0" ]; then
  echo -e "${S_ERR}: patch directory contains no patch file (*${MY_PATCH_EXT}) - ${MY_PATCH_DIR}${_NC}"
  exit 1
fi

# check repo is clean
MY_IS_CLEAN=$(git status -s --untracked-files=no 2>&1)
if [ -n "${MY_IS_CLEAN}" ]; then
  echo -e "${S_ERR}: make sure you've committed all pending changes${_NC}"
  exit 1
fi

# check branch exists
_=$(git rev-parse --verify ${MY_LOCAL_BRANCH} 2>&1)
if [ "$?" -eq "0" ]; then
  if [ "${MY_DEBUG_REMOVE_LOCAL_BRANCH}" == "" ]; then
    echo -e "${S_ERR}: local branch \"${MY_LOCAL_BRANCH}\" already exists${_NC}"
    exit 1
  fi
  echo -e "${_BC}Checking out branch \"${MY_DEBUG_REMOVE_LOCAL_BRANCH}\"..${_NC}"
  git checkout ${MY_DEBUG_REMOVE_LOCAL_BRANCH}
  if [ "$?" -ne "0" ]; then
    echo -e "${S_ERR}: failed to checkout branch \"${MY_DEBUG_REMOVE_LOCAL_BRANCH}\"${_NC}"
    exit 1
  fi
  echo -e "${_BC}Removing local branch \"${MY_LOCAL_BRANCH}\"..${_NC}"
  git branch --delete --force ${MY_LOCAL_BRANCH}
  if [ "$?" -ne "0" ]; then
    echo -e "${S_ERR}: failed to delete local branch \"${MY_LOCAL_BRANCH}\"${_NC}"
    exit 1
  fi
fi

# fetch repo
echo -e "${_BC}Fetching..${_NC}"
git fetch
if [ "$?" -ne "0" ]; then
  echo -e "${S_ERR}: failed to fetch"
  exit 1
fi

# create local branch
echo -e "${_BC}Creating local branch${_NC}"
git checkout -b ${MY_LOCAL_BRANCH} origin/${MY_REMOTE_BRANCH}
if [ "$?" -ne "0" ]; then
  echo -e "${S_ERR}: failed to create local branch${_NC}"
  exit 1
fi

# apply patches
MY_CNT_PATCH_FILES=0
for filename in ${MY_PATCH_DIR}/*${MY_PATCH_EXT}; do
  if [ ! -f "${filename}" ]; then
    continue
  fi
  echo "Applying ${filename}"
  git am -q <${filename}
  if [ "$?" -ne "0" ]; then
    echo -e "${S_ERR}: failed to apply patch - ${filename}${_NC}"
    exit 1
  fi
  MY_CNT_PATCH_FILES=$((MY_CNT_PATCH_FILES+1))
done
echo -e "${_BC}Applied ${MY_CNT_PATCH_FILES} files${_NC}"
if [ "${MY_CNT_PATCH_FILES}" -eq "0" ]; then
  echo -e "${S_ERR}: no patch was applied from - ${MY_PATCH_DIR}${_NC}"
  exit 1
fi

# just list commits
echo -e "${_BC}Here's the git log:${_NC}"
git log -n${MY_CNT_PATCH_FILES}
if [ "$?" -ne "0" ]; then
  echo -e "${S_ERR}: git log failed - weird${_NC}"
  exit 1
fi

# now push commits
echo -e "${_BC}Pushing commits to $(git config remote.origin.url)${_NC}"
git push origin ${MY_LOCAL_BRANCH}:${MY_LOCAL_BRANCH}
if [ "$?" -ne "0" ]; then
  echo -e "${S_ERR}: git push failed - weird${_NC}"
  exit 1
fi

echo -e "${_BC}.have a nice day.${_NC}"
echo -e "${_BC}.done.${_NC}"
