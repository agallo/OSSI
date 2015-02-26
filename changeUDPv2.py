#!/usr/bin/python

__author__ = 'agallo'


'''
the extension file must be a list of 5 digit extensions
one per line.  no checking is done to ensure that the
entries are valid dial plan extensions or even numbers
it must always be called extfile.  the output is always
extfile.ossi and will be overwritten if it exists
'''
extensions = open('extfile', 'r')
outfile = open('extfile.ossi', 'w')

# declare field addresses
# these are the CM database addresses used to identify
# different fields within CM forms
matchingpattern = "f6c01ff01"
length = "fec36ff01"
delete = "fec37ff01"
insert = "f6c02ff01"
net    = "f6c03ff01"


def extsanitycheck():
    counter = 1
    for line in extensions:
        if not isinstance(line, int):
            print "error on line ", counter, '. ', line, ' is not an integer'
        counter += 1


# reading extensions from the file:
# splitlines was used rather than 'for each line in' because
# that format included the newline character, which was
# printed in the output file, resulting in an uneeded blank line
# when reading with split lists, a list was created, and [0] retrieves
# the first value


def createOSSI():
    print "entering createOSSI"
    for line in extensions:
        print "entering for loop"
        currext = line.splitlines()[0]
        print >> outfile, 'cchange uniform-dialplan', currext
        print >> outfile, matchingpattern
        print >> outfile, '%s%s' % ('d', currext)
        print >> outfile, length
        print >> outfile, "%s%s" % ('d', '5')
        print >> outfile, delete
        print >> outfile, "%s%s" % ('d', '1')
        print >> outfile, insert
        print >> outfile, "%s%s" % ('d', '142')
        print >> outfile, net
        print >> outfile, "%s%s" % ('d', 'aar')
        print >> outfile, 't'
        print >> outfile


def main():
    extsanitycheck()
    createOSSI()

main()

extensions.close()
outfile.close()
