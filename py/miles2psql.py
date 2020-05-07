#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE

#############################################################################
# 
#  /home/git/clones/SAS2019/Miles/maketable.py
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
import copy
# (wg-python-graphics)
__doc__ = """

/home/git/clones/SAS2019/Miles/maketable.py
[options] files...



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
   clean_quotes = re.compile(r'\'')
   clean_spaces = re.compile(r'[ ]+')
   clean_dots   = re.compile(r'[./]')
   basedict = {'INSTRUME'   : None,  # rounded up the values the hard way.
               'ORIGIN'     : None,
               'DATE'       : None,
               'MID_TU'     : None,
               'EXP_TIME'   : None,
               'ID'         : None,
               'A1996_80'   : None,
               'D1996_80'   : None,
               'BERV'       : None,
               'RV'         : None,
               'SIGMA_RV'   : None,
               'MEAN_S_N'   : None,
               'A2000_00'   : None,
               'D2000_00'   : None,
               'A1996_00'   : None,
               'D1996_00'   : None,
               'A1950_00'   : None,
               'D1950_00'   : None
              }
   missing_keys = {}
   rawtable = {}      # {filename : {basedictcopy}}
   for filename in args:
      with open(filename,'r') if filename else sys.stdin as f:
         entry = copy.deepcopy(basedict)
         for rawl in f:
            l = rawl.strip()
            if(l == ""):
               break
            rawparts = list(map(str.strip,l.split('=')) )
            parts1 = list(map(lambda a: clean_quotes.sub('',a),rawparts))
            parts2 = (clean_spaces.sub('_',parts1[0]),parts1[1])
            parts  = (clean_dots  .sub('_',parts2[0]),parts2[1])
            try:
               k = parts[0]
               if(k not in basedict):
                  if(k not in missing_keys):
                     missing_keys[k] = []
                  missing_keys[k].append(filename)
            except Exception as e:
               print("caught: ",parts[0],missing_keys,e)
               raise
            val = ''
            if(parts[1] is None):
               val = 'NULL'
            else:
               val = "{}".format(parts[1])  # coerce value to staring
            if(k == 'ID'):
               val = clean_spaces.sub('',val)
            entry[k] = val
      rawtable[filename] = entry
      
   for k,v in missing_keys.items():
      print("Missing key: {:12s} {:5d}".format(k,len(v)),file=sys.stderr)

   #print("Len of rawtable {}".format(len(rawtable)))
   ###################################################################
   #  Make the database table
   ###################################################################
   createstmt = """\\c wayne
/*****************************************************************************
* raw_miles_flux_corrected
*****************************************************************************/
DROP TABLE    IF EXISTS raw_miles_flux_corrected;
DROP SEQUENCE IF EXISTS raw_miles_flux_corrected_sequence;
CREATE SEQUENCE         raw_miles_flux_corrected_sequence START 100000;

CREATE TABLE raw_miles_flux_corrected (
   uniqueid     integer PRIMARY KEY DEFAULT nextval('raw_miles_flux_corrected_sequence'),
   filename     text,
{}
);
COMMENT ON TABLE raw_miles_flux_corrected is 'Miles flux calibrated spectra';
"""
   insertstmt = """INSERT INTO raw_miles_flux_corrected ({}) VALUES"""
   insert_list = ['filename']
   create_body = []
   for filename,entry in rawtable.items():  # {filename, dict}
      for k,v in entry.items():
         if(v is None):
            entry[k] = 'NULL'
         insert_list.append(k)
         create_body.append("   {:10s}   text".format(k))
      break
   print(createstmt.format(',\n'.join(create_body)))

   print(insertstmt.format(', '.join(insert_list)))
   comma = ""
   for filename,entry in rawtable.items():  # {filename, dict}
      value_list = ["'{}'".format(filename)]
      for k,v in entry.items():
         if(v is None):
            v = 'NULL'
            value_list.append(v)
         else:
            value_list.append("'{}'".format(v.strip()))
      try:
         print("{}   ( {:s} ) ".format(comma, ','.join(value_list)), end="")
      except Exception as e:
         print("Oops, {}".format(entry))
         raise
      comma = ",\n"
   print(";")
   
   
       



