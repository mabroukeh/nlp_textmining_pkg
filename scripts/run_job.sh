#!/bin/bash
#
#  Job Specification v1.3
#

## Determine which data center we are in
. /opt/ampjobs/conf/get_datacenter.sh || exit 1
## Load environment variables
. /opt/ampjobs/conf/setenv.sh -n dsci-pub-pubsmart2 -t cron || exit 1

## Log Cleanup
JOB_clean  ## Clears up ${JOB_LOGHOME} and ${JOB_TMPHOME}

# Begin
cd ${JOB_HOME}

# Setting a default exit code
JOB_EXITCODE=0

# Set python path
source /opt/amp-anaconda2-4.0.0/bin/activate root
export PYTHONPATH=$JOB_HOME/python:$JOB_HOME/resources:$JOB_HOME/libs/python:$PYTHONPATH

# Python
python ${JOB_HOME}/python/interface.py ${PARAMS_STRING} "$@"
JOB_EXITCODE=$[$JOB_EXITCODE+$?]

## Any logs you create should go in $JOB_LOGHOME
date >> ${JOB_LOGHOME}/date.log

## End
JOB_printLogs  # Prints out the contents of all files in $JOB_LOGHOME
exit ${JOB_EXITCODE}
