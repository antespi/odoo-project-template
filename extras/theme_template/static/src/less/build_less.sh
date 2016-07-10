#!/bin/bash
# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# LESS='/usr/bin/lessc --clean-css --no-js --no-color'
LESS='/usr/bin/lessc --no-js --silent'

compile() {
    local from="$1"
    local to="$2"
    local error=0

    echo -n "Compiling $from -> $to ... "
    $LESS "$from" "$to"
    error=$?
    if [ $error -eq 0 ]; then
        echo "OK"
    else
        echo "ERROR($error)"
    fi
}

LIST=(
    theme
    # options/colors/xxx
)

for index in `seq 0 1 $((${#LIST[@]} - 1))`; do
    compile "${LIST[$index]}.less" "${LIST[$index]}.css"
done
