#!/bin/bash

DEBUG=0
PARAMS=1

FIND=/usr/bin/find
LN=/bin/ln
GREP=/bin/grep
READLINK=/bin/readlink
DIRNAME=/usr/bin/dirname

if [ ! $# -ge $PARAMS ]; then
    echo "Usage: $0 <repo_path>"
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

for i in $@; do
    REPO_PATH="$i"

    if [ ! -d "$REPO_PATH" ]; then
        echo "ERROR : Repository path '$REPO_PATH' not found"
    fi

    REPO_PATH=`$READLINK -m $REPO_PATH`

    cd $ROOT_PATH
    addons=`$FIND "$REPO_PATH" -maxdepth 2 -mindepth 2 -type f -name __openerp__.py | sed 's/\/__openerp__.py//' | sed 's/^.*\///'`

    for f in $addons ; do
        if [ -e "$f" ]; then
            echo "'$f' already exists"
        else
            echo "Adding '$f'"
            ln -s "$REPO_PATH/$f" "$f" ;
        fi
    done
done