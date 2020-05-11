#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE
# MAINMAINMAIN

 
#############################################################################
# fits2psqlraw
#
# ls -1 *fits > input.txt # 7421 files
# fits2psqlraw --list input.txt -D wayne -t myfits -c
#
#  /home/git/clones/NGSL/data/stis_xxx/fits2psqlraw
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
#
# (iv (setq tmp (/ 7421.0  (+ (* 60.0 8) 11.847 ))))  15.088 records per second
#############################################################################
import optparse              # we're flexible about our sources etc.
import os
import re                    # idiots put single quotes in comments
import sys                   # because  sys!
from astropy.io import fits  # open file, deal with the header
import json                  # json data
import collections           # use an ordered dict, keep cards in order
import pprint
from .utils import *          # cleanpath,cleantarget,s2r,s2d,pquote

# (wg-python-graphics)
__doc__ = """
fits2psqlraw  [options] files...

ls -1 \*fits > table.idx
fits2psqlraw -D mydb -t mynewtable --list table.idx

./fits2psqlraw -D wayne -t rawngslheaders --target=TARGNAME --index \*fits > rawngslheaders.psql

Given a FITS files on on the command line or -T <filename> with fits
files, one per line with blank lines and sharp to end of line ignored,
dig out the header(s) and make a json structure of the headers. Produce
a 'raw' '.psql' file capable of being loaded as a data script to stdout.
It is 'raw' in the sense that it captures the image as-is. CREATE/SELECT/JOIN
and/or INSERT/SELECT/JOIN can transliterate these raw data into the
main collection.

Multiple FITS extensions are supported. No FITS data embedded, 

Tfree main questions reflected in the data record:
Where (ra,dec)
What (the target's name)
and the file's fully qualified original name.

A "-n, --basepath" switch gives a key directory name, default is
'Observations'. For the actual path to the file, say,
"/home/edwin/Observations/25Dec2012/focus/foc.0001.fits"
the fqpn will be "25Dec2012/focus/foc.0001.fits" with
NO leading slash. 

The target name will have leading/trailing spaces
removed, intermediate spaces compressed into one
space. 

Some 'Philisophy' is needed here. 

The --ra <keyword> --dec <keyword> options take precedence and RA and
DEC keywords used by default if they exist, else NULL. (In some
reference images, there is no hint of the ra/dec only a target name).

The --target <keyword> takes presidence. If not the default OBJECT is
used if found, else NULL.

Support extended HDUs within the JSON structure
as {  hdu0 : {header json} [, hdun : {header 1+ json} }.

This program sends output to stdout.

Command Line flags
==================
-b, --basepath   str      the part from / down to the base directory.
-c, --create     bool     create table and Q3C index
-t, --table      str      table name
-D, --database   str      database name
-v, --verbose    bool     be verbose about work
-w, --write      str      fqpath filename for a psql image
--list           str      file of files; one fqpathname per line

Keyword Fields
--------------
--ra             str      keyword of the RA field  e.g.: TARGRA
--dec            str      keyword of the DEC field
--target         str      keyword of the Target's catalog name.

OK,,, a FITS header, ala AstroPY, is a 'card' consisting of a tuple of
3 things: a keyword, a value, and a comment.  A Python dictionary is a
(key,value) pair. So we make an insert statement that carries a
PostgreSQL 'jsonb' datatype, with the 'key' from the fits files
together with a nested 'jsonb' structure consisting of 'value' and
'comment' for the card.  The comment information carries important
data.

q3c_radial_query(tablera, tabledec, queryra, querydec, radiusdegrees)

Here are some sample queries:

.. code-block:: psql
   :linenos:

   select count(*) from myfits;
   select ora,odec from myfits limit 10;
   
   select fqpname,ora::numeric(7,5),odec::numeric(7,5) from myfits
      where q3c_radial_query(ora, odec, 9.7419958, 48.3369, 0.1);
   
   -- Acid test with timing examples

   \\timing
   select header->'OBJECT' ->> 'value' as "OBJECT",
          fqpname,
          ora::numeric(7,5) as "RA",
          odec::numeric(7,5) as "Dec",
          COALESCE(header->'FILTER' ->> 'value' as "Filter"),     -- force NULL if json fails.
          COALESCE(header->'DATE-OBS'  ->> 'value'  as "dateobs")
   from myfits
      where q3c_radial_query(ora, odec, 9.7419958, 48.3369, 0.1)
      order by header->'FILTER'->> 'value',header->'DATE-OBS'->> 'value';
   \\timing


.. csv-table:: "Query Example"
   :header"  "OBJECT", "fqpname", "RA", "Dec", "Filter", "dateobs"
   :widths"  18,40,12,12,12,32

   'NGC185'  , elp1m008-kb74-20140525-0059-e90.fits , 9.74200 , 48.33700 , 'ip'   , '2014-05-26T10:50:17.539'
   'NGC185'  , elp1m008-kb74-20140525-0060-e90.fits , 9.74200 , 48.33701 , 'ip'   , '2014-05-26T10:52:14.272'
   'NGC185'  , elp1m008-kb74-20140624-0048-e90.fits , 9.74200 , 48.33700 , 'ip'   , '2014-06-25T09:14:32.307'
   'NGC185'  , elp1m008-kb74-20140624-0049-e90.fits , 9.74199 , 48.33698 , 'ip'   , '2014-06-25T09:16:28.901'
   'NGC185'  , elp1m008-kb74-20140919-0035-e90.fits , 9.74200 , 48.33699 , 'ip'   , '2014-09-20T08:29:59.623'
   'NGC185'  , elp1m008-kb74-20140919-0036-e90.fits , 9.74200 , 48.33699 , 'ip'   , '2014-09-20T08:31:56.280'
   'NGC0185' , elp1m008-kb74-20141026-0084-e90.fits , 9.74199 , 48.33699 , 'ip'   , '2014-10-27T01:59:41.961'
   'NGC0185' , elp1m008-kb74-20141026-0085-e90.fits , 9.74198 , 48.33700 , 'ip'   , '2014-10-27T02:01:39.030'
   'NGC0185' , elp1m008-kb74-20141113-0148-e90.fits , 9.74201 , 48.33703 , 'ip'   , '2014-11-14T08:04:45.533'
   'NGC0185' , elp1m008-kb74-20141113-0149-e90.fits , 9.74199 , 48.33701 , 'ip'   , '2014-11-14T08:06:41.930'
   'NGC0185' , elp1m008-kb74-20141213-0212-e90.fits , 9.74200 , 48.33700 , 'ip'   , '2014-12-14T06:05:21.695'
   'NGC0185' , elp1m008-kb74-20141213-0213-e90.fits , 9.74199 , 48.33701 , 'ip'   , '2014-12-14T06:07:18.217'
   'NGC0185' , elp1m008-kb74-20150119-0112-e90.fits , 9.74199 , 48.33697 , 'ip'   , '2015-01-20T03:35:00.511'
   'NGC0185' , elp1m008-kb74-20150119-0113-e90.fits , 9.74199 , 48.33696 , 'ip'   , '2015-01-20T03:36:57.501'
   'NGC0185' , elp1m008-kb74-20141026-0086-e90.fits , 9.74200 , 48.33701 , 'rp'   , '2014-10-27T02:03:46.954'
   'NGC0185' , elp1m008-kb74-20141026-0087-e90.fits , 9.74201 , 48.33701 , 'rp'   , '2014-10-27T02:05:43.386'
   'NGC0185' , elp1m008-kb74-20141113-0150-e90.fits , 9.74200 , 48.33701 , 'rp'   , '2014-11-14T08:08:50.869'
   'NGC0185' , elp1m008-kb74-20141113-0151-e90.fits , 9.74200 , 48.33696 , 'rp'   , '2014-11-14T08:10:47.421'
   'NGC0185' , elp1m008-kb74-20141213-0214-e90.fits , 9.74200 , 48.33699 , 'rp'   , '2014-12-14T06:09:26.973'
   'NGC0185' , elp1m008-kb74-20141213-0215-e90.fits , 9.74201 , 48.33700 , 'rp'   , '2014-12-14T06:11:24.220'
   'NGC0185' , elp1m008-kb74-20150119-0114-e90.fits , 9.74201 , 48.33699 , 'rp'   , '2015-01-20T03:39:05.758'
   'NGC0185' , elp1m008-kb74-20150119-0115-e90.fits , 9.74200 , 48.33699 , 'rp'   , '2015-01-20T03:41:03.008'

Time: 12.903 ms

Taking Sergey's advice, and re-timing the query:
   

.. code-block:: psql
   :linenos:

   \\timing
   select header->'OBJECT' ->> 'value' as "OBJECT",
          fqpname,
          ora::numeric(7,5) as "RA",
          odec::numeric(7,5) as "Dec",
          header->'FILTER' ->> 'value' as "Filter",
          header->'DATE-OBS'  ->> 'value'  as dateobs
   from myfits
      where q3c_join(9.7419958, 48.3369, ora, odec, 0.1)
      order by header->'FILTER'->> 'value',header->'DATE-OBS'->> 'value';
   \\timing

Time: 9.848 ms 

% (iv (setq tmp (/ 12.903 9.848 )))   1.31 speed up.

See https://github.com/segasai/q3c for details.

Notes
=====

The code to fix path names is here, just unused.
Target names are 'fixed' down to one space to stand the best chance
of a match with SIMBAD. Please use actual SIMBAD names.

The output is 'raw' for a reason, any changes to the filename,
or header values should come later. For example, a new header
may be created with campaign specific headers while the
old header's JSON structure may be retained.

"""


__author__  = 'Wayne Green'
__version__ = '1.0'


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
if __name__ == "__main__":
   opts = optparse.OptionParser(usage="%prog "+__doc__)

#   opts.add_option("-", "--", action="store", dest="",
#                   default=,
#                   help="<>     .")

   opts.add_option("-c", "--create", action="store_true", dest="create",
                   default=False,
                   help="<bool>     create table.")

   opts.add_option("-D", "--database", action="store", dest="database",
                   default='database',
                   help="<str>   database name.")

   opts.add_option("-i", "--index", action="store_true", dest="index",
                   default=False,
                   help="<bool>     create table.")

   opts.add_option("-s", "--schema", action="store", dest="schema",
                   default='public',
                   help="<str>   schema name else public .")

   opts.add_option("-t", "--table", action="store", dest="table",
                   default='table',
                   help="<str>   table name.")

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

   opts.add_option("-w", "--write", action="store", dest="write",
                   default=None,
                   help="<str>     output file name for \\i <includepsqlfile>....")

   opts.add_option("--basepath", action="store", dest="basepath",
                   default=None,
                   help="<str>     remove the base from filename.")

   opts.add_option("--list", action="store", dest="list",
                   default=None,
                   help="<str>     file with 1 filename per line")

   opts.add_option("--ra", action="store", dest="rakeyword",
                   default='RA',
                   help="<str>     The keyword identifying the RA field")

   opts.add_option("--dec", action="store", dest="deckeyword",
                   default='DEC',
                   help="<str>     the keyword identifying the Dec field")

   opts.add_option("--target", action="store", dest="targetkeyword",
                   default='OBJECT',
                   help="<str>     the keyword identifying the target name field")

   (options, args) = opts.parse_args()


   ###################################################################
   #  Load list of files (command line is only so big! Adds list
   # to any found on the command line.
   ###################################################################
   if(options.list is not None):
      with open(options.list,'r') as f:
         for l in f:
            fname = l.split('#')[0].strip()
            args.append(l.strip())

   ###################################################################
   #  Get the options local and formatted.
   ###################################################################

   schema        = options.schema
   table         = options.table                          # collec the options values.
   database      = options.database
   rakeyword     = options.rakeyword
   deckeyword    = options.deckeyword
   targetkeyword = options.targetkeyword
   basepath      = options.basepath

   ###################################################################
   #  The create statement. Pretty simple.
   #  Make a raw table, then select from that into a working table
   # if needed. Indexing at the bottom of this file.
   ###################################################################
   createquery = """\\c {0}\n
CREATE SCHEMA IF NOT EXISTS {1};
DROP TABLE IF EXISTS    {1}.{2} CASCADE;
DROP SEQUENCE IF EXISTS {1}.{2}_sequence;
CREATE SEQUENCE         {1}.{2}_sequence START 100000;

CREATE TABLE {1}.{2} (
   uniqueid  integer PRIMARY KEY DEFAULT nextval('{2}_sequence'),
   fqpname   text,             -- fully qualified path name
   target    text,             -- the target name or NULL
   ora       double precision, -- raw ra  (if we can find one)
   odec      double precision, -- raw dec (if we can find one)
   nhdu      integer,          -- count of ndu in complex json field [0,1,...,n-1]
   header    jsonb             -- json binary image of fits header
);
COMMENT ON TABLE {1}.{2}          is 'Raw FITS file name and its header.';
COMMENT ON COLUMN {1}.{2}.fqpname is 'fully qualified path name';
COMMENT ON COLUMN {1}.{2}.target  is 'Cleaned target name';
COMMENT ON COLUMN {1}.{2}.ora     is 'ra [decimal degrees]';
COMMENT ON COLUMN {1}.{2}.odec    is 'dec [decimal degrees]';
COMMENT ON COLUMN {1}.{2}.nhdu    is 'number of HDUs';
COMMENT ON COLUMN {1}.{2}.header  is 'PostgreSQL jsonb header';

""".format(database,schema,table)                                # database extablished with connection

   insertstmt    = "INSERT INTO {}.".format(schema) + "{} (ora, odec, target, fqpname, nhdu, header) values ( {}, {}, '{}', '{}', {}, '{}' );\n"
   ofile         = sys.stdout                             # output file as needed
 
   if(options.write is not None):                         # default the output to stdout
      ofile = open(options.write,'w')
   print(createquery,file=ofile)     # get the top part of psql file out

   ###################################################################
   #  Process each file.
   #  Assume only one HDU perfile, Ignore the data.
   ###################################################################
# MAINMAINMAIN
   msgs = []
   for filename in args: # PDB-DEBUG
      try:
         fqpn = os.path.abspath(filename)                    # determine a fqpn
         if(basepath is not None):
            parts = fqpn.split(basepath)
            fqpn = '/'.join(parts[1:])                       # all but the first one
         if(fqpn[0] is '/'):
            fqpn = fqpn[1:]                                  # do not permit leading slash
   
         records     = collections.OrderedDict()             # all the hdu's for this file.
         tblvalues   = []
         if(options.verboseflag):
            print("File {}".format(filename))
         f           = fits.open(filename)
         raval       = decval = target = 'NULL'              # grab the first hint of a RA/DEC This file.
   
         for hduidx,hdu in enumerate(f):                     # the list of hdus, get one.
            h        = hdu.header
            history  = []                                    # initialize structures for this file
            comment  = []                                    # aggregate history anc comments for file
            myheader = collections.OrderedDict()             # collect json bound header's values
      
            ################################################################
            #  Load up an ordered dictionary for the cards, aggregate the
            #  history and comments in order.
            ################################################################
            for c in h.cards:
               key = c.keyword
               if(type(c.value) is type("") and "'" in c.value):
                  c.value = _requote.sub(",",c.value)
               elif('Undefined' in "{}".format(type(c.value))):
                  c.value = 'NULL' # PDB-DEBUG
                  msgs.append("Warning File {:s}[{:d}] keyword {:s} undefined, set to NULL".format(filename,hduidx,c.keyword))
               if(type(c.comment) is type("") and "'" in c.comment):
                  c.comment = _requote.sub("",c.comment)
               if(options.verboseflag): print("|{}|  |{}|  ".format(key,c.value))
               if(key == 'HISTORY'):
                  history.append(c.value)
                  if(options.verboseflag):
                     print("HISTORY keyword |{}| value |{}| c.comment |{}|".format(key, c.value, c.comment))
               elif(key == 'COMMENT'):
                  history.append(c.value)
                  if(options.verboseflag):
                     print("COMMENT keyword |{}| value |{}| c.comment |{}|".format(key, c.value, c.comment))
               elif(key != ''):  # the tail end of a 'block', Astropy's interesting artifact!
                  myheader[key] = {'value' : pquote(c.value), 'comment' : pquote(c.comment)}   # HEREHEREHERE
                  #myheader[key] = '{'+ "{},{}".format(pquote(c.value), pquote(c.comment)) + '}'
                  #myheader[key] = '{{"value" : {}, "comment" : {}}}'.format(c.value,c.comment) # examples
                  if(key == rakeyword):
                     if(type(c.value) == type('str')):
                        myheader[key] = s2r(c.value)         # change to decimal if ra
                     else:
                        myheader[key] = c.value
                  elif(key == deckeyword):
                     if(type(c.value) == type('str')):
                        myheader[key] = s2d(c.value)         # or dec
                     else:
                        myheader[key] = c.value
                  elif(key == targetkeyword):
                     if(type(c.value)):
                        myheader[targetkeyword] = c.value    # or dec
         
            if(len(history) != 0):                           # add any history statements 
               myheader['HISTORY'] = "HISTORY "+ ",HISTORY ".join(history)
      
            if(len(comment) != 0):                           # add any comment statements
               myheader['COMMENT'] = "COMMENT " + ",COMMENT ".join(comment)
            # end of cards for one hdu element of a file.   
      
            if(rakeyword in myheader and raval == 'NULL'):   # pick up the dfirst one
               raval = "{:8.5f}".format(myheader[rakeyword])
            if(deckeyword in myheader and decval == 'NULL'):
               decval = "{:8.5f}".format(myheader[deckeyword]) # string as raw
            if(targetkeyword in myheader and target == 'NULL'):
               target = "{}".format(myheader[targetkeyword])
   
            if(len(tblvalues) == 0):
               tblvalues = [raval,decval,fqpn]
            records['HDU[{}]'.format(hduidx)] = myheader
            
         # records is an ordered dict, by 'HDU[{}]' arrays raval,decval,filename,myheader
         hduidx     += 1                                     # hduidx bump to cardinal number
         jd          = json.dumps(records)                   # make the json part.
         insertquery = insertstmt.format(table,raval,decval,target,filename,hduidx,jd)
         print(insertquery,file=ofile)
         # end of this filename's header
      except Exception as e:
         print ("Exception with {:s}[{:d}] - {:s}".format(filename, hduidx, e.__str__()),file=sys.stderr)
         print("Card {}".format(c),file=sys.stderr)
         pprint.pprint(records,stream=sys.stderr,indent=3)


   ###################################################################
   #  Prepare the indexing.
   ###################################################################

   q3cquery = """
CREATE INDEX ON {0}      (public.q3c_ang2ipix(ora,odec)); -- {0}_q3c_ang2ipix_idx
CLUSTER {0}_q3c_ang2ipix_idx      ON {0};
ANALYZE  {0};

"""
   
   if(options.index):
      print(q3cquery.format(table),file=ofile)
      print("commit",file=ofile)
      ofile.close()

   if(len(msgs) != 0):
      print('\n'.join(msgs),file=sys.stderr)

"""

select target, r2s(ora) as "RA", d2s(odec) as "DEC",
       quote_literal(header -> 'HDU[0]' -> 'GRATING' ->> 'value') as "Grating",
       quote_literal(header -> 'HDU[0]' -> 'SPECTYPE' ->> 'value') as "SpType"
from rawngslheaders
where header -> 'HDU[0]' -> 'SPECTYPE' ->> 'value' = 'composite'
order by ora::integer/15,odec
;


select jsonb_object_keys(hdu) from
(select header -> 'HDU[0]' as "hdu"
  from rawngslheaders
  limit 1) xx
;

select jsonb_object_keys(hdu) from
(select header -> 'HDU[1]' as "hdu"
  from rawngslheaders
  limit 1) xx
;

-- Tie in the SIMBAD data with topcat

select ora, odec from rawngslheaders;

"""
