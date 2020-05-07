#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
# 
#  /home/git/clones/NGSL/doc/Chanti.tex
#
#emacs helpers
# (insert (buffer-file-name))
#
# (ediff-current-file)
# (wg-python-fix-pdbrc)
# (find-file-other-frame "./.pdbrc")
# (wg-python-fix-pdbrc)   # PDB DASH DEBUG end-comments
# (when (fboundp 'electric-indent-mode) (electric-indent-mode -1))
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
import ChiantiPy.core as ch
import numpy as np
import matplotlib.pyplot as plt
# (wg-python-graphics)
__doc__ = """

/home/git/clones/NGSL/doc/Chanti.tex
[options] files...

export XUVTOP=/home/wayne/Configuration/ChiantiPy

   t = 10.**(5.8 + 0.05*np.arange(21.))
   
   fe14 = ch.ion('fe_14', temperature=t, eDensity=1.e+9, em=1.e+27)
   
   fe14.popPlot()

"""


__author__  = 'Wayne Green'
__version__ = '0.1'



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

   t = 10.**(5.8 + 0.05*np.arange(21.))
   
   fe14 = ch.ion('fe_14', temperature=t, eDensity=1.e+9, em=1.e+27)
   
   fe14.popPlot()


