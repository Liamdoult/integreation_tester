#!/bin/bash

DIR=${1:-.}
LINES=$(yapf -d -r "${DIR}" | wc -l | tr -s ' ')

if [ ${LINES} -eq 0 ]; then
    echo "Yapf PASS"
else
    echo "Yapf FAIL"
fi

exit ${LINES}