#!/bin/bash

# Re-orders the networkProfiler scan types so they display in order when
# querying the types of scans available
# This expects to be run out of utils in the release package.

mydir=`dirname $0`

scandir="${mydir}/../LP/lpconfig/m0d000000/predefinedScans"
scansavedir="${scandir}.save"

if [ -n "$1" ]
then
    echo "Usage: $0"
    echo "  Re-orders the networkProfiler scans so they show up in order in the LP."
    echo "  This script should not be copied; it should be run in the directory it came in in the release package."
    exit 1
fi

if [ ! -d "${scandir}" ]
then
    echo "I can't find the scan directory: I expected it to be in \"${scandir}\". If you copied this script file somewhere else, please put it back where it came from and run it from there."
    exit 1
fi

if [ -e "${scansavedir}" ]
then
    echo "The backup directory \"${scansavedir}\" already exists. Have you run this script before? If you really want to run the script again, please rename this directory to something else."
    exit 1
fi

\mv -f ${scandir} ${scansavedir}
if [ $? -ne 0 ]
then
    echo "Unable to save off predefinedScans directory \"${scandir}\" to \"${scansavedir}\". Terminating."
    exit 1
fi

\mkdir ${scandir}
if [ $? -ne 0 ]
then
    echo "Unable to create new predefinedScans directory \"${scandir}\". Terminating."
    \mv -f ${scansavedir} ${scandir}
    exit 1
fi

for fname in MAC2MAC srcIP srcMACIP IP2IP IP2IP_bytes TCPUDP TCPSYN TCPUDP_bytes
do
    \mv -f ${scansavedir}/${fname} ${scandir}
    if [ $? -ne 0 ]
    then
        echo "Unable to properly copy scan $fname. Terminating."
        \mv -f ${scandir}/* ${scansavedir}
        \rmdir ${scandir}
        \mv -f ${scansavedir} ${scandir}
        exit 1
    fi
done

for fname in TCPUDP_condense TCPUDP_condense_bytes TCPSYN_condense TCPSYN_condense_bytes
do
    for condenserange in 256 512 1024 1536 2048 2560 3072
    do
        \mv -f ${scansavedir}/${fname}_${condenserange} ${scandir}
        if [ $? -ne 0 ]
        then
            echo "Unable to properly copy scan ${fname}_${condenserange}. Terminating."
            \mv -f ${scandir}/* ${scansavedir}
            \rmdir ${scandir}
            \mv -f ${scansavedir} ${scandir}
            exit 1
        fi
    done
done

# copy over anything that might be left
\mv -f ${scansavedir}/* ${scandir}
\rmdir ${scansavedir}

echo "Operation successful."

