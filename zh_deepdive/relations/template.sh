#!/usr/bin/env bash

TEMPLATE_DIR="$1"
DESTINATION_DIR="$2"


# cp
cp -r ${TEMPLATE_DIR} ${DESTINATION_DIR}

# udf
cd ${DESTINATION_DIR}/udf
chmod +x *.py

cd ../
chmod +x evaluation.py
chmod +x load_data.py
chmod +x load_data_top_negative.py

# run
rm -rf ${DESTINATION_DIR}/run

# input
rm -rf ${DESTINATION_DIR}/input/*


rm ${DESTINATION_DIR}/predict.json
rm ${DESTINATION_DIR}/evaluation.result
