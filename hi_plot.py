#!/usr/bin/env python

"""
# hi_plot.py


Jonathan Zwart
September 2014

Usage:

./hi_plot.py config_file.ini

"""

import sys
import time
import os
import pprint
from hibayes.parse_config import parse_config
import pylab

# if os.getenv('PBS_O_HOST') is not None and 'baltasar' not in os.getenv('PBS_O_HOST'):
from hibayes import contour_plot

if os.getenv('PBS_O_HOST') not in [None, 'baltasar']:
    import pylab
from hibayes.utils import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'usage:'
        print './hi_plot.py config_filename.ini'
        print
        sys.exit(0)

param_file = sys.argv[-1]
# load runtime parameters
rp = parse_config(param_file)


#-------------------------------------------------------------------------------


@profile
def main():
    """
    """

    print 'Settings file is %s' % param_file

    # Import the settings variables
    #set_module = importlib.import_module(setf)
    #globals().update(set_module.__dict__)

    # Insert hacks here
    #plotRanges['C']=[0,200]
    #    triangle='triangle_%s.png' %outdir		# original
    triangle = 'triangle.pdf'
    #triangle = 'triangle_%s.pdf' % rp["outdir"]
    #    autoscale=True	# comment back for original
    autoscale = False

    chain = pylab.loadtxt('%s/1-post_equal_weights.dat' % rp["outdir"])
    bundle = contour_plot.contourTri(chain,
                                     line=True, outfile='%s/%s' % (rp["outdir"], triangle),
                                     col=('red', 'blue'), labels=rp["parameters"],
                                     ranges=rp["plotRanges"], autoscale=autoscale)
    #bundle=contour_plot.contourTri(chain,\
    #                        line=True,outfile='%s/%s'%(outdir,triangle),\
    #                        col=('red','blue'),labels=parameters,\
    #                        ranges=plotRanges,truth=plotTruth,autoscale=True,\
    #                        title='%s - %s'%(outdir,dataset))

    print '-> Now open %s/%s' % (rp["outdir"], triangle)

    # Plot for publication
    line = False
    autoscale = True
    title = ''
    truth = None
    extn = 'pdf'
    binsize = 25
    bundle = contour_plot.contourTri(chain,
                                     line=line,
                                     outfile='%s/triangle-publn.%s' % (rp["outdir"], extn),
                                     labels=rp["parameters"],
                                     ranges=rp["plotRanges"], truth=truth,
                                     autoscale=autoscale, title=title,
                                     binsize=binsize, labelDict=rp["labelDict"])

    stats = fetchStats(rp["outdir"], rp["parameters"], rp["plotTruth"])
    printLaTeX(rp["parameters"], stats, dump=rp["outdir"])

    return 0

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
