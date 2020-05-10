#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
#
# (wg-python-toc)
#
#
# def cleanpath(fqpname:'filepath')->'clean filepath': # cleanpath()
#
# def cleantarget(target:'str to clean')->'str': # cleantarget()
#
# def s2r(rastr:'RA sexigesimal')  ->'RA decimal degrees':  # s2r()
#
# def s2d(decstr:'DEC sexigesimal')->'DEC decimal Degrees':  # s2d()
#
# def pquote(str:'str to psql quote')->'quote_literal(str)': # pquote()
#
#
#               
#############################################################################
import optparse
import re
import sys
# (wg-python-graphics)

__all__ = ['cleanpath','cleantarget','s2r','s2d','pquote']

__doc__ = """ 
uils.py -- collect common utility functions shared between these
packages here. These are real common, but author hates wheels within
wheels.

"""


__author__  = 'Wayne Green'
__version__ = '0.1'

_coordre   = re.compile(r'[dmsh: ]+')  # convert sexigesimal for several formats.
_requote   = re.compile(r'\'')         # remove single quotes from comments.
_refixpath = re.compile(r'[ &\']+')     # characters to replace

##############################################################################
# cleanpath - rules to clean the pathname
#
##############################################################################
def cleanpath(fqpname:'filepath')->'clean filepath': # cleanpath()
   """Replace one or more spaces or special characters with a single underscore
   Args:   fqpname(str)  path to clean.

   Returns:
           string with spaces and special characters fixed.
   """
   ret = fqpname
   if(type(fqpname) == type("")):
      ret = _refixpath.sub('_',fqpname)
   return ret

# cleanpath

##############################################################################
# cleantarget- rules to clean the target name.
#
##############################################################################
def cleantarget(target:'str to clean')->'str': # cleantarget()
   """Replace one or more spaces or special characters with a single underscore
   Args:

   Returns:

   """
   ret = target
   if(type(target) == type("")):
      ret = _refixpath.sub('_',target)
   return ret

#   cleantarget

##############################################################################
# s2r -- convert sexigesimal right ascension to degrees
#
##############################################################################
def s2r(rastr:'RA sexigesimal')  ->'RA decimal degrees':  # s2r()
   """s2r - convert a sexadecimal RA TO a floating point degrees.  input
   is string hh:mm[:ss.s] Will take ra.ddddd ra:mm.mmm as well.
   The truncated forms appear in SIMBAD query output.
   Args:

   Returns:

   
   """
   ra = None
   try:
      parts = [x for x in _coordre.split(rastr) if x != ''] + ['0','0','0']# dang trailing s
      parts = list(map(float,parts[:3]))
      if(len(parts) == 1):
         ra = parts[0] * 15.0     # a straight hrs.xxxxxxx
      elif(len(parts) == 2):
         ra = (parts[0] + (parts[1] / 60.0)) * 15.0
      elif(len(parts) == 3):
         ra = (parts[0] + (parts[1] / 60.0) + parts[2]/3600.0) * 15.0
   except:
      print("r2d: parts{}".format(parts),file=sys.stderr)
      raise Exception("s2r: Unable to convert %s to degrees ra" % rastr)
   return ra

### s2r rastr='+01 06 40'

##############################################################################
# s2d -- convert sexigesimal declination to degrees
#
##############################################################################
def s2d(decstr:'DEC sexigesimal')->'DEC decimal Degrees':  # s2d()
   """s2d - convert a sexadecimal Dec TO a floating point degrees.  input
   is string hh:mm[:ss.s] Will take ra.ddddd ra:mm.mmm as well.
   The truncated forms appear in SIMBAD query output.
   Args:

   Returns:

   

   """
   sign = 1.0
   try:
      parts = [x for x in _coordre.split(decstr) if x != ''] + ['0','0','0']# dang trailing s
      parts = list(map(float,parts[:3]))
      if(parts[0] < 0.0):
         sign = -1.0
         parts[0] = -1 * parts[0]
      if(len(parts) == 1):
         dec = parts[0]     # a straight d.xxxxxxx
      elif(len(parts) == 2): # d m.xxxxxx
         dec = (parts[0] + (parts[1] / 60.0))
      elif(len(parts) == 3): # d m s.xxxx
         dec = (parts[0] + (parts[1] / 60.0) + parts[2]/3600.0)
   except:
      print("r2d: Unable to convert sexigesimal %s to degrees dec {}".format(decstr),
            file=sys.stderr)
      print("r2d: parts{}".format(parts),file=sys.stderr)
      raise Exception("r2d: Unable to convert sexigesimal %s to degrees dec" % decstr)
   return sign*dec

### s2d

##############################################################################
# plquote -- if str is a string, then return a single quoted value.
#  at this point, the quotes have been removed.
##############################################################################
def pquote(str:'str to psql quote')->'quote_literal(str)': # pquote()
   """Return a quoted string if str is a string.
   Args:  str(str)  The string to wrap with double quotes.

   Returns:
          str  - in effect the PostgreSQL quote_literal function. Handy
                 when parsing input data for psql json.

   """
   ret = str
   return ret
   if(type(str) is type("")):
      ret = "'{}'".format(str)
   return ret

### pquote


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

# regression tests when we get to them.
