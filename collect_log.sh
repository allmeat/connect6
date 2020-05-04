#!/usr/bin/env bash
PROJECT_HOME=$(cd `dirname $0` && pwd)
cd ${PROJECT_HOME}

PYTHONPATH=${PROJECT_HOME}/playground:${PYTHONPATH}
PYTHONPATH=${PROJECT_HOME}/repo:${PYTHONPATH}
export PYTHONPATH

if [ $# -lt 1 ]
  then
    echo "usage: ./collect_log.sh {number of simulation}"
    exit
fi
NUM="$1"
python repo/collect_log.py ${NUM}