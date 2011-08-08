#!/usr/bin/python
# Copyright (c) 2011 C. R. Oldham <cro@ncbt.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
import pysmug
import logging
import __builtin__
from optparse import OptionParser

from pysmug.keywords import smugmug_keyword

logger = logging.getLogger(__name__)

def Usage(parser):
    parser.print_help()
    
def main(argv=None):
    if argv is None:
        argv = sys.argv

    p = OptionParser(usage="usage: %prog [options] AlbumID AlbumKey\n       %prog [options] AlbumID_AlbumKey\n  (second usage is handy for copy/paste from a SmugMug URL).\n  Username and password are stored in ~/.pysmug.")
    p.add_option("-q", "--quiet", dest="quiet",
        default=False, action="store_true", help="Don't display names of images downloaded.")
    opts, args = p.parse_args()
    
    if len(args) == 1 and args[0].find("_"):
        idandkey = args[0].split("_")
        albumid = idandkey[0]
        albumkey = idandkey[1]
    elif len(args) == 2:
        albumid = args[0]
        albumkey = args[1]
    elif len(args) < 1 or len(args) > 2 or opts.help == True:
        Usage(p)
        return(-1)

    m = pysmug.login()
    b = m.batch()
    if (opts.quiet == False):
        print "Downloading..."
    total_images = 0
    for album, image in b.images_download(AlbumID=albumid, AlbumKey=albumkey):
        if (opts.quiet == False):
            targetfilename = image['Image']['FileName'].split("/")[-1]
            print targetfilename + ": " + image['stat']
        total_images += 1
        
    if (opts.quiet == False):
        print "Total images: " + str(total_images)
        
    return 0;
    
if __name__ == "__main__":
    sys.exit(main())
