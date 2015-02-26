__author__ = 'agallo'


from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Script to generate an OSSI file for mass"
                                    " Uniform Dialing Plan (UDP) changes")


parser.add_argument('-i', '--infile', dest='extfile',
                    help="specify input file. Default is extfile",
                    default='extensions')
parser.add_argument('-o', '--outfile', dest='outfile',
                    help="specify output file. Default is extfile.OSSI",
                    default='extfile.OSSI')
parser.add_argument('-c', '--checktype', dest='checktype',
                    help='Sanity checking type. Default is strict (die if file is not clean)',
                    default='strict')
args = parser.parse_args()


extensions = open(args.extfile, 'r')
outfile = open(args.outfile, 'w')

sanity = args.checktype

failcount = 0
successcount = 0

# declare field addresses
# these are the CM database addresses used to identify
# different fields within CM forms
matchingpattern = "f6c01ff01"
length = "fec36ff01"
delete = "fec37ff01"
insert = "f6c02ff01"
net    = "f6c03ff01"


def extsanitycheck():
    global failcount
    counter = 1
    for line in extensions:
        try:
            int(line)
        except ValueError:
            failcount += 1
        counter += 1
    return failcount


# reading extensions from the file:
# splitlines was used rather than 'for each line in' because
# that format included the newline character, which was
# printed in the output file, resulting in an uneeded blank line
# when reading with split lists, a list was created, and [0] retrieves
# the first value


def createOSSI():
    extensions.seek(0)
    currentline = 0
    global successcount
    global failcount
    failcount = 0
    for line in extensions:
        currentline += 1
        currext = line.splitlines()[0]
        try:
            int(currext)
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
            successcount += 1
        except:
            failcount += 1

    return successcount, failcount


def main():
    extsanitycheck()
    if failcount > 0 and sanity == 'strict':
        print
        print '****not creating OSSI file because it isn\'t clean.'
        print 'There are ', failcount, 'errors in the file.\nPlease correct them.'
        outfile.close()
        os.remove(args.outfile)
    else:
        createOSSI()
        print "Processed ", successcount, ' extensions.'
        print failcount, "lines were skipped because of errors on the line."
        print "OSSI file is ", args.outfile



main()

extensions.close()
outfile.close()