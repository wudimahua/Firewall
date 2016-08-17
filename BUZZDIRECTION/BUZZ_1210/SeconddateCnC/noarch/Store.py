#!/usr/bin/env python

"""
This is a python implementation of the Store utility.
This is to configure BinStore implants on any platform.
"""

import sys
import struct
import getopt
import MixText

USAGE="""
Usage: Store.py <action> --file=<path to BinStore implant>

Possible actions:
   --set=NAME              sets a value into the binary (if
                           neither --value or --valueFromFile
                           options are supplied the value is read
                           from STDIN)
                           
   --value=VALUE           use a specified VALUE as a string (this
                           will get null terminated automatically)
                           
   --valueFromFile=VALUE   read the value from a file as raw bytes,
                           the file contents will NOT be null terminated.
                           
   --list                  list the current name/value pairs in the implant.
   
   --wipe                  wipe the configuration from the implant

For example:
  echo -ne \"value\\xff\\xfe\\x43\\x00\" | Store.py --set=\"name\" --file=\"myfile\"
  Store.py --set=\"name\" --value=\"value\" --file=\"myfile\"
  Store.py --list --file=myfile
  Store.py --wipe --file=myfile
"""

"""
These header and footer values deliniate the start and end of
the BinStore package within a binary.
"""
BINSTORE_PACKAGE_HEADER_HEX = '\xe2\xd7\x88\x6a\x81\x0d\xbf\x98'
BINSTORE_PACKAGE_FOOTER_HEX = '\x6b\x4e\x95\x65\x84\x06\x2a\x5f'

"""
struct BinStorePayloadHeader
{
    Lla_U32 version ;
    /** The total size of the data within the payload (excluding the payload
     * header).  Equal to the BINSTORE_PAYLOAD_SIZE. */
    Lla_U64 size ;
    /** Munged or unmunged data, duplicates, etc. */
    /** Flag_t is an Lla_U32 */
    Flag_t flags ;
    /** The offset into the first item from the start of the payload. */
    Lla_U64 itemOffset ;
} __attribute__((packed)) ;
"""
BINSTORE_PAYLOAD_STRUCT = '>IQIQ'

"""
struct BinStoreDataName
{
    Lla_U64 size ;
    /** Offset from the start of the payload. */
    Lla_U64 offset ;
} __attribute__((packed)) ;

struct BinStoreDataValue
{
    Lla_U64 size ;
    /** Offset from the start of the payload. */
    Lla_U64 offset ;
} __attribute__((packed)) ;

/* Since the previous structures are contained within the DataItem, they
 * should be of a static size. */
struct BinStoreDataItem
{
    struct BinStoreDataName name ;
    struct BinStoreDataValue value ;
    /** Offset from the start of the payload. */
    Lla_U64 nextOffset ;
} ;
"""
BINSTORE_DATAITEM_STRUCT = '>QQQQQ'

def ALIGN8(N):
    return (N) + (8 - ( (N) % 8 ))


"""
Builds a BinStore package from a python dictionary.

map - a dict of name/value pairs which will get mapped into a BinStore package
size - the size of the BinStore package to create

returns the new BinStore package.
"""
def buildPackage(map, size):
    package = ""
    numKeys = len(map.keys( ))
    i = 0

    if numKeys == 0:
        firstOffset = 0
    else:
        firstOffset = struct.calcsize(BINSTORE_PAYLOAD_STRUCT)
        
    package += struct.pack(
        BINSTORE_PAYLOAD_STRUCT,
        3,
        size,
        0x00000000,
        firstOffset)
    
    for name in map.keys( ):
        value = map[name]
        name = MixText.mix(name, 0x42)
        value = MixText.mix(value, 0x42)
        
        nameLen = len(name)
        valueLen = len(value)
        nameLenActual = ALIGN8(nameLen)
        valueLenActual = ALIGN8(valueLen)

        nameOffset = len(package) + struct.calcsize(BINSTORE_DATAITEM_STRUCT)
        valueOffset = nameOffset + nameLenActual

        if i != (numKeys-1):
            nextOffset = valueOffset + valueLenActual
        else:
            nextOffset = 0

        package += struct.pack(
            BINSTORE_DATAITEM_STRUCT,
            nameLen,
            nameOffset,
            valueLen,
            valueOffset,
            nextOffset)

        package += name
        package += '\x00'*(nameLenActual - nameLen)

        package += value
        package += '\x00'*(valueLenActual - valueLen)
        "file=",
        i += 1

    if len(package) > size:
        raise Exception, "The data to store is bigger than the BinStore package allows"
    
    package += '\x00'*(size - len(package))

    return package
        
"""
Returns the raw BinStore package from a file buffer.

buf - the file's contents from which you want to extract the BinStore package.

returns a tuple:
   1. The package data
   2. The start offset of the package within the file buffer
   3. The end offset of the package within the file buffer
"""
def getPackage(buf):
    headerIndex = buf.find(BINSTORE_PACKAGE_HEADER_HEX)

    if headerIndex == -1:
        raise Exception, "Could not find BinStore header."

    footerIndex = buf.find(BINSTORE_PACKAGE_FOOTER_HEX)

    if footerIndex == -1:
        raise Exception, "Could not find BinStore footer."


    size = footerIndex - (headerIndex + len(BINSTORE_PACKAGE_HEADER_HEX))

    # print "Found a BinStore package of %d bytes" % size

    package = buf[(headerIndex + len(BINSTORE_PACKAGE_HEADER_HEX)):footerIndex]

    return (package, (headerIndex + len(BINSTORE_PACKAGE_HEADER_HEX)), footerIndex)

"""
This reads an individual data item from the BinStore package at the
specified offset.

returns a tuple:
   1. the name of the data item
   2. the value of the data item
   3. the offset into the package where the next data item is
"""
def getDataItem(package, offset):
    
    (nameSize, nameOffset, valueSize, valueOffset, nextOffset) = struct.unpack(
        BINSTORE_DATAITEM_STRUCT,
        package[offset:][:struct.calcsize(BINSTORE_DATAITEM_STRUCT)])

    name = package[nameOffset:][:nameSize]
    value = package[valueOffset:][:valueSize]
    name = MixText.unmix(name)
    value = MixText.unmix(value)

    return (name, value, nextOffset)


"""
This will actually write a generataed package to a file.

filename - the file to write the new BinStore package to
newPackage - the new BinStore package.

No return value, exception on error.
"""
def insertNewPackage(fileBuf, newPackage):
    (existingPackage, start, end) = getPackage(fileBuf)

    if len(existingPackage) != len(newPackage):
        raise Exception, (
            "Existing package is %d bytes, new package is %d bytes" %
            (len(existingPackage), len(newPackage)))

    newFileBuf = fileBuf[0:start]
    newFileBuf += newPackage
    newFileBuf += fileBuf[end:]

    return newFileBuf

"""
This will read name/value pairs from a BinStore package and
return a python 'dict' (a.k.a. a hashtable) of the values.

fileBuf - the entire file's contents where the BinStore package reides.

returns a dict with the package's contents
"""
def readValues(fileBuf):
    nameValueMap = { }
    (package, start, end) = getPackage(fileBuf)

    (version, size, flags, itemOffset) = struct.unpack(
        BINSTORE_PAYLOAD_STRUCT,
        package[0:][0:struct.calcsize(BINSTORE_PAYLOAD_STRUCT)])

    if version != 3:
        raise Exception, "Only know how to work with v3 BinStore"

    if itemOffset == 0:
        return { }
    
    (name, value, nextOffset) = getDataItem(package, itemOffset)

    nameValueMap[name] = value

    while nextOffset != 0:
        (name, value, nextOffset) = getDataItem(package, nextOffset)
        nameValueMap[name] = value

    return nameValueMap
    
"""
Sets a name/value pair into the BinStore package.

fileBuf - a buf containing the entire file's contents
name - the name to set
value - the value to set

returns a new file buffer containing the new name/value pair.
"""
def setValue(fileBuf, name, value):
    nameValueMap = readValues(fileBuf)

    (package, start, end) = getPackage(fileBuf)

    nameValueMap[name] = value

    newPackage = buildPackage(nameValueMap, len(package))

    if len(newPackage) != len(package):
        raise Exception, "New package is not the same length as original"

    newFileBuf = insertNewPackage(fileBuf, newPackage)

    return newFileBuf

"""
Adds multiple name/value pairs to a fileBuf.  Essentially
calls setValue repeatedly on each name/value pair in the
dictionary supplied.

fileBuf - a buffer representing the entire file.
nameValueMap - a dict containing name/value pairs to
    add into the BinStore package

returns a new file buffer containing the new values
"""
def setValues(fileBuf, nameValueMap):
    newFileBuf = fileBuf
    
    for name in nameValueMap.keys( ):
        newFileBuf = setValue(
            newFileBuf,
            name,
            nameValueMap[name])
        
    return newFileBuf

"""
Removes all name/value pairs from the BinStore package
in the file buffer supplied.

fileBuf - a buffer representing the entire file

returns a new file buffer with the BinStore package null'd out.
"""
def wipe(fileBuf):
    (currentPackage, start, end) = getPackage(fileBuf)
        
    nullPackage = buildPackage({ }, len(currentPackage))
    
    newFileBuf = insertNewPackage(fileBuf, nullPackage)

    return newFileBuf


"""
Entrypoint for the command line Store utility.
"""
def main( ):

    if len(sys.argv) < 2:
        print "You need to supply arguments."
        print USAGE
        sys.exit(-1)
        
    try:
        (opts, args) = getopt.getopt(
            sys.argv[1:],
            "",
            ["file=",
             "set=",
             "value=",
             "valueFromFile=",
             "list",
             "wipe"])
    except getopt.GetoptError, err:
        print str(err)
        print USAGE
        sys.exit(-1)

    oList = False
    oWipe = False
    oFilename = None
    oSet = None
    oValue = None
    oValueFromFile = None
    
    for option, value in opts:
        if option == "--file":
            oFilename = value
        elif option == "--set":
            oSet = value
        elif option == "--value":
            oValue = value
        elif option == "--valueFromFile":
            oValueFromFile = value
        elif option == "--list":
            oList = True
        elif option == "--wipe":
            oWipe = True

    if oFilename != None:
        f = open(oFilename, 'rb')
        fileBuf = f.read( )
        f.close( )
    else:
        raise Exception, "A file name must be supplied for any action."

    if oWipe == True:
        newFileBuf = wipe(fileBuf)

        f = open(oFilename, 'wb')
        f.write(newFileBuf)
        f.close( ) 

    if oSet != None:
        if oValue == None and oValueFromFile == None:
            print "Reading value from STDIN... "
            oValue = sys.stdin.read( )
            print "Read %d bytes from STDIN." % len(oValue)
        elif oValue == None and oValueFromFile != None:
            f = open(oValueFromFile, 'rb')
            oValue = f.read( )
            f.close( )
        else:
            oValue += '\x00'
                        
        newFileBuf = setValue(fileBuf, oSet, oValue)

        f = open(oFilename, 'wb')
        f.write(newFileBuf)

    if oList == True:
        nameValueMap = readValues( fileBuf )

        print "\n"
        for key in nameValueMap.keys( ):
            value = nameValueMap[key]
            print "  %s \t => \t  [%s]" % (key, value)
            

if __name__ == "__main__":
    main( )
