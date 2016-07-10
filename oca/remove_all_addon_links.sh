#!/bin/bash

DEBUG=0
PARAMS=0

FIND=/usr/bin/find
LN=/bin/ln
GREP=/bin/grep
READLINK=/bin/readlink
DIRNAME=/usr/bin/dirname
XARGS=/usr/bin/xargs
RM=/bin/rm

if [ ! $# -ge $PARAMS ]; then
    echo "Usage: $0"
    exit 1;
fi

root_path() {
    SOURCE="${BASH_SOURCE[0]}"
    DIR="$( dirname "$SOURCE" )"
    while [ -h "$SOURCE" ]
    do
        SOURCE="$( readlink "$SOURCE" )"
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
        DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd )"
    done
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

    echo "$DIR"
}

ROOT_PATH=`root_path`

echo -n "Removing all symlinks in '$ROOT_PATH' folder ... "
$FIND "$ROOT_PATH" -type l -print0 | $XARGS -0 -r $RM -rf
echo "Done"
