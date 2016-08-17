#! /usr/bin/env python

import sys
import re

def decode_status(date_string):
    m = re.search('(\d{2}):(\d{2}):(\d{2})\.(\d{3})',date_string);
    if( m == None ):
        return -1;
    hh=m.groups()[0];
    mm=m.groups()[1];
    ss=m.groups()[2];
    ms=m.groups()[3];
    nhh=int(hh,10);
    nmm=int(mm,10);
    nss=int(ss,10);
    nms=int(ms,10);
    result = nms - ((nhh*nmm*nss) % 1000);
    if( result < 0 ):
        result += 1000;
    return result;


def usage():
    print 'Usage: %s <date> [ <date2> [ <date3> ... ] ]' % sys.argv[0]

if len(sys.argv) == 1:
    usage()

for arg in sys.argv:
    ret = decode_status(arg)
    if( ret != -1 ):
        print '%s: %d' % (arg,ret)


