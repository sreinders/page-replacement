import getopt
import random
import sys

# default values if no command line arguments supplied
pages = 5
length = 10

def usage():
    print("""
        pagerefgen.py [--pages = npages] [--length = nrefs]

        This program generates a random sequence of page numbers.  The page
        numbers are drawn from a logical address space containing npages
        pages.  The sequence will be of length nrefs.

        npages = the number of pages in the virtual address space
        nrefs  = the total number of page references in the address string
    """)

def generate(n, l):
    """method to be called externally to generate page number sequence"""
    seq = []
    for count in range(l):
        nextref = random.randint(0, n-1)
        seq.append(nextref)
    return seq

if __name__ == '__main__':
    """to be executed if command line arguments are supplied"""
    (vals, path) = getopt.getopt(sys.argv[1:], 'p:l:', ['pages=','length='])
    for (opt, val) in vals:
        if opt == '-p' or opt == '--pages':
            pages = int(val)
        if opt == '-l' or opt == '--length':
            length = int(val)
    if len(path) != 0:
        usage()
        sys.exit(1)
    seq = map(str, generate(pages, length))
    for s in seq:
        print("%s" % s)
