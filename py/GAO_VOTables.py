#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
# 
#  /home/wayne
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
#
# class TOPCAT_VOTableException(Exception):
#    def __init__(self,message,errors=None):
#    @staticmethod
#    def __format__(e):
#
# class TOPCAT_VOTable:  # TOPCAT_VOTable(object) if inherited
#    def __init__(self,filename):                       # TOPCAT_VOTable::__init__()
#    def debug(self,msg="",os=sys.stderr):           # TOPCAT_VOTable::debug()
#
# class GAIA_VOTableException(Exception):
#    def __init__(self,message,errors=None):
#    @staticmethod
#    def __format__(e):
#
# class GAIA_VOTable:  # GAIA_VOTable(object) if inherited
#    def __init__(self,filename):                               # GAIA_VOTable::__init__()
#    def debug(self,msg="",os=sys.stderr):           # GAIA_VOTable::debug()
#
#
#               
#############################################################################
import optparse
import re
import sys
import numpy as np
#import pyvo as vo
from astropy.io.votable import parse
__all__ = ["TOPCAT_VOTableException","TOPCAT_VOTable","GAIA_VOTableException","GAIA_VOTable"]

# (wg-python-graphics)
__doc__ = """

/home/wayne
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'


##############################################################################
# TOPCAT_VOTableException
#
##############################################################################
class TOPCAT_VOTableException(Exception):
   """Special exception to allow differentiated capture of exceptions"""
   def __init__(self,message,errors=None):
      super(TOPCAT_VOTableException,self).__init__("TOPCAT_VOTable "+ message)
      self.errors = errors
   @staticmethod
   def __format__(e):
      return "TOPCAT_VOTable" % e
# TOPCAT_VOTableException



##############################################################################
# TOPCAT_VOTable
#
##############################################################################
class TOPCAT_VOTable:  # TOPCAT_VOTable(object) if inherited
   """ A base class/simple wrapper for a votable.
   """

   def __init__(self,filename):                       # TOPCAT_VOTable::__init__()
      """Initialize this class."""
      #super(base,self).__init__()
      #self.
      self.filename = filename
      self.votable  = parse('CastorGAIA.vo')
      self.table    = votable.get_first_table().to_table(use_names_over_ids=True)
      self.colnames = table.keys()

   ### TOPCAT_VOTable.__init__()


   def debug(self,msg="",os=sys.stderr):           # TOPCAT_VOTable::debug()
      """Help with momentary debugging, file to fit."""
      print("TOPCAT_VOTable - %s " % msg, file=os)
      for key,value in self.__dict__.items():
         print("%20s = %s" % (key,value),file=os)

      return self

   ### TOPCAT_VOTable.debug()

   __TOPCAT_VOTable_debug = debug  # preserve our debug name if we're inherited

# class TOPCAT_VOTable

##############################################################################
# GAIA_VOTableException
#
##############################################################################
class GAIA_VOTableException(Exception):
   """Special exception to allow differentiated capture of exceptions
"""
   def __init__(self,message,errors=None):
      super(GAIA_VOTableException,self).__init__("GAIA_VOTable "+ message)
      self.errors = errors
   @staticmethod
   def __format__(e):
      return "GAIA_VOTable" % e
# GAIA_VOTableException


##############################################################################
# GAIA_VOTable
#
##############################################################################
class GAIA_VOTable:  # GAIA_VOTable(object) if inherited
   """ Extend the basic table for GAIA via Aladin SAMP contribution.
   '_RAJ2000'
   '_DEJ2000'
   '_V'
   'RA_ICRS'
   'e_RA_ICRS'
   'DE_ICRS'
   'e_DE_ICRS'
   'Source'
   'Plx'
   'e_Plx'
   'pmRA'
   'e_pmRA'
   'pmDE'
   'e_pmDE'
   'Dup'
   'FG'
   'e_FG'
   'Gmag'
   'e_Gmag'
   'FBP'
   'e_FBP'
   'BPmag'
   'e_BPmag'
   'FRP'
   'e_FRP'
   'RPmag'
   'e_RPmag'
   'BP-RP'
   'RV'
   'e_RV'
   'Teff'
   'AG'
   'E(BP-RP)'
   'Rad'
   'Lum'
   
   """

   def __init__(self,filename):                               # GAIA_VOTable::__init__()
      """Initialize this class."""
      super(base,self).__init__(filename)
      #self.
      self.ra     = self.table['_RAJ2000']
      self.dec    = self.table['_DEJ2000']
      self.GMag   = self.table['Gmag']
      self.BPMag  = self.table['BPmag']
      self.RPmag  = self.table['RPmag']

   ### GAIA_VOTable.__init__()


   def debug(self,msg="",os=sys.stderr):           # GAIA_VOTable::debug()
      """Help with momentary debugging, file to fit."""
      __TOPCAT_VOTable_debug.debug(msg="",os=sys.stderr)
      print("GAIA_VOTable - %s " % msg, file=os)
      for key,value in self.__dict__.items():
         print("%20s = %s" % (key,value),file=os)

      return self

   ### GAIA_VOTable.debug()

   __GAIA_VOTable_debug = debug  # preserve our debug name if we're inherited

# class GAIA_VOTable





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



