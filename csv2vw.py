'Convert CSV file to vw format. Headers can be skipped with argv[4] == true.'
'-1 for label index if no label in file'

import sys
import csv
import argparse

def construct_line( label, line ):
    new_line = []
    try:
        label = float( label )
    except Exception, e:
        pass

    if label == 0.0:
        label = "0"
    new_line.append( "%s |n " % ( label ))

    for i, item in enumerate( line ):
        try:
            item = float( item )
        except ValueError, e:
            pass
        if item == 0.0:
            continue    # sparse!!!
        new_item = "%s:%s" % ( i + 1, item )
        new_line.append( new_item )
    new_line = " ".join( new_line )
    new_line += "\n"
    return new_line

# ---

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help = "path to csv input file")
parser.add_argument("output_file", help = "path to output file")


parser.add_argument("-l", "--label_index", help = "specify index of label col", type=int,
                    default = -1)

parser.add_argument("-s", "--skip_headers", help = "specify if there are headers in the file - default false",
                     action="store_true")

args = parser.parse_args()

input_file = sys.argv[1]
output_file = sys.argv[2]


i = open( input_file )
o = open( output_file, 'w' )

reader = csv.reader( i )
if args.skip_headers:
    headers = reader.next()

n = 0

for line in reader:
    if args.label_index == -1:
        label = 1
    else:
        label = line.pop( args.label_index )

    new_line = construct_line( label, line )
    o.write( new_line )

    n += 1
    if n % 10000 == 0:
        print n


