#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
# 
#  /home/git/pre/pre.NGSL_SAS/py/bessel1983.py
#
#emacs helpers
# (insert (buffer-file-name))
#
# (ediff-current-file)
# (wg-python-fix-pdbrc)
# (find-file-other-frame "./.pdbrc")
# (wg-python-fix-pdbrc)   # PDB DASH DEBUG end-comments
#
# (setq mypdbcmd (concat (buffer-file-name) "<args...>"))
# (progn (wg-python-fix-pdbrc) (pdb mypdbcmd))
#
# (wg-astroconda-pdb)       # IRAF27
# (wg-astroconda3-pdb)      # CONDA Python3
#
# (set-background-color "light blue")
# (wg-python-toc)
#               
#############################################################################
import optparse
import re
import sys
import numpy as np
# (wg-python-graphics)
__doc__ = """

/home/git/pre/pre.NGSL_SAS/py/bessel1983.py
[options] files...


"""

ignore = """
Bessell
http://articles.adsabs.harvard.edu/pdf/1983PASP...95..480B table II
(setq vfilter ( list 0.0 0.0 0.03 0.084 0.163 0.301 0.458 0.630 0.78
                0.895 0.967 0.997 1.0 0.988 0.958 0.919 0.877 0.819
                0.765 0.711 0.657 0.602 0.545 0.488 0.434 0.386 0.331
                0.289 0.25 0.214 0.181 0.151 0.12 0.093 0.069 0.051
                0.036 0.027 0.021 0.018 0.016 0.014 0.012 0.011 0.01
                0.009 0.008 0.007 0.003 0.005 0.004 0.003 0.002 0.001
                0.0))
(setq offs 470)
(mapcar (lambda (b) (progn (insert (format "[ %8.3f, %7.3f ],\n" offs b)) (setq offs (+ offs 5.0)))) vfilter)

"""


__author__  = 'Wayne Green'
__version__ = '0.1'

bessel_vfilter = np.array([ [  470.000,   0.000 ],
                            [  475.000,   0.000 ],
                            [  480.000,   0.030 ],
                            [  485.000,   0.084 ],
                            [  490.000,   0.163 ],
                            [  495.000,   0.301 ],
                            [  500.000,   0.458 ],
                            [  505.000,   0.630 ],
                            [  510.000,   0.780 ],
                            [  515.000,   0.895 ],
                            [  520.000,   0.967 ],
                            [  525.000,   0.997 ],
                            [  530.000,   1.000 ],
                            [  535.000,   0.988 ],
                            [  540.000,   0.958 ],
                            [  545.000,   0.919 ],
                            [  550.000,   0.877 ],
                            [  555.000,   0.819 ],
                            [  560.000,   0.765 ],
                            [  565.000,   0.711 ],
                            [  570.000,   0.657 ],
                            [  575.000,   0.602 ],
                            [  580.000,   0.545 ],
                            [  585.000,   0.488 ],
                            [  590.000,   0.434 ],
                            [  595.000,   0.386 ],
                            [  600.000,   0.331 ],
                            [  605.000,   0.289 ],
                            [  610.000,   0.250 ],
                            [  615.000,   0.214 ],
                            [  620.000,   0.181 ],
                            [  625.000,   0.151 ],
                            [  630.000,   0.120 ],
                            [  635.000,   0.093 ],
                            [  640.000,   0.069 ],
                            [  645.000,   0.051 ],
                            [  650.000,   0.036 ],
                            [  655.000,   0.027 ],
                            [  660.000,   0.021 ],
                            [  665.000,   0.018 ],
                            [  670.000,   0.016 ],
                            [  675.000,   0.014 ],
                            [  680.000,   0.012 ],
                            [  685.000,   0.011 ],
                            [  690.000,   0.010 ],
                            [  695.000,   0.009 ],
                            [  700.000,   0.008 ],
                            [  705.000,   0.007 ],
                            [  710.000,   0.003 ],
                            [  715.000,   0.005 ],
                            [  720.000,   0.004 ],
                            [  725.000,   0.003 ],
                            [  730.000,   0.002 ],
                            [  735.000,   0.001 ],
                            [  740.000,   0.000 ]
                 ])

def integrate1():
   """Do the rectangular integratino of the function.
   """
   x                    = bessel_vfilter[:,0] # wavelength bins
   percent_transmission = bessel_vfilter[:,1] # percent transmission



##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
   opts = optparse.OptionParser(usage="%prog "+__doc__)

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

   (options, args) = opts.parse_args()

   #if(len(args) == 0 ): args.append(None)
   for filename in args:
      with open(filename,'r') if filename else sys.stdin as f:
         for l in f:
            if('#' in l):
               continue
            parts = map(str.strip,l.split()) 



