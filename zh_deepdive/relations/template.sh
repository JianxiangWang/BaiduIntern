#!/usr/bin/env bash

TEMPLATE_DIR="$1"
DESTINATION_DIR="$2"


# cp
cp -r ${TEMPLATE_DIR} ${DESTINATION_DIR}

# udf
cd ${DESTINATION_DIR}/udf
chmod +x *.py

# run
rm -rf ${DESTINATION_DIR}/run
