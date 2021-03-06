#!/usr/bin/env python3
# -*- coding: latin-1 -*-
# HEREHEREHERE
# examples
#############################################################################
# json2psql /home/wayne/git/clones/SAS2019/Miles/data/json2psql#SIMBAD_MILES_Missing.query#
# TGAS_1581296149784O-result.json
#
# ls -1 *fits > input.txt # 7421 files
# fits2sqljson --list input.txt -D wayne -t myfits -c
#
#  /home/wayne/JSON2SQL.py
#
# (find-file-other-frame "./.pdbrc")
#
# (wg-python-fix-pdbrc) # PDB DASH -DEBUG end-comments
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
# class ADQL_JSON_PSQLException(Exception):
#    def __init__(self,message,errors=None):
#    @staticmethod
#    def __format__(e):
#
# class ADQL_JSON_PSQL:  # ADQL_JSON_PSQL(object) if inherited
#    def __init__(self, tablename, db_description, jsonfile):           # ADQL_JSON_PSQL::__init__()
#    def debug(self,msg="",os=sys.stderr):             # ADQL_JSON_PSQL::debug()
#    def maketable_definition(self):                   # ADQL_JSON_PSQL::maketable_definition()
#    def make_inserts(self):                           # ADQL_JSON_PSQL::make_inserts()
#    def log_error(self,line,field,value,dtype):       # ADQL_JSON_PSQL::log_error()
#    def sanity_check_data(self,line,field,value,dtype): # ADQL_JSON_PSQL.sanity_check_data()
#    def insert(self):                                 # ADQL_JSON_PSQL::insert()
#    def db_load(self):                                # # ADQL_JSON_PSQL::db_load()
#    def writepsqlfile(self):                          # ADQL_JSON_PSQL::writepsqlfile()
#
#############################################################################
import optparse              # we're flexible about our sources etc.
import re                    # idiots put single quotes in comments
import sys                   # because  sys!
import json                  # json data
import psycopg2              # ah, postgresql
import collections           # use an ordered dict, keep cards in order
import getpass               # Shuuuush! we're secret!
from .utils import s2r,s2d,pquote

__all__ = ["ADQL_JSON_PSQLException","ADQL_JSON_PSQL"]


# (wg-python-graphics)
__doc__ = """

json2psql  [options] files...

json2psql -D mydb -t mynewtable

Asks for password for the user. if -u/--user omitted then
the user's name is taken from system login information.

-D, --database   str   database name
-t, --table      str   table name
-u, --username   str   username, defaults to login id
-w, --write      str   fqpath filename for a psql image
--host           str   host [localhost]
--port           str   port address
-v, --verbose    bool  be verbose about work

This program assumes installation nativly or a container that has
Ubuntu 18.04 LTE, postgreSQL 11 and https://github.com/segasai/q3c
installed. (really fast indexing).

Given a filename for a JSON structure returned from a TAP
query, where the keys are 'metadata' and 'data'; construct
the create table clause from the metadata, and message
the json into a format suitable for direct insertion into
the database.

"""


__author__  = 'Wayne Green'
__version__ = '1.0'

##############################################################################
# ADQL_JSON_PSQLException
#
##############################################################################
class ADQL_JSON_PSQLException(Exception):
   """Special exception to allow differentiated capture of exceptions"""
   def __init__(self,message,errors=None):
      super(ADQL_JSON_PSQLException,self).__init__("ADQL_JSON_PSQL "+ message)
      self.errors = errors
   @staticmethod
   def __format__(e):
      return "ADQL_JSON_PSQL" % e
# ADQL_JSON_PSQLException



##############################################################################
# ADQL_JSON_PSQL
#
##############################################################################
class ADQL_JSON_PSQL:  # ADQL_JSON_PSQL(object) if inherited
   """ Given the json from ADQL (TGAS for now) query, make the table.

   """
   table_declaration = """/*****************************************************************************
* {0}
*****************************************************************************/
DROP TABLE    IF EXISTS {0};
DROP SEQUENCE IF EXISTS {0}_sequence;
CREATE SEQUENCE         {0}_sequence START 100000;

CREATE TABLE {0} (
   uniqueid  integer PRIMARY KEY DEFAULT nextval('{0}_sequence'),
{1}
);
"""

   insert_statement = """INSERT INTO {0} ({1}) VALUES"""
   fixnulls         = re.compile(r'null')
   integercheck     = re.compile(r'^[0-9]+$')
   floatcheck       = re.compile(r'^[0-9][.eEfFgG+-][0-9]+')
   fixquotes        = re.compile(r'["]')

   def __init__(self, tablename, db_description, jsonfile):           # ADQL_JSON_PSQL::__init__()
      """Initialize this class."""
      #super(base,self).__init__()
      self.db_description  = db_description
      self.tablename       = tablename
      self.jsonfile        = jsonfile
      self.json            = None
      self.fieldnames      = []           # build field names and types in parallel
      self.fieldtypes      = []           # in order. Fieldtypes later for insert
      self.createstmt      = None
      self.insertstmt      = None
      self.errors          = []
      self.insertquery     = None
      self.json = json.load(open(self.jsonfile,'r'))

      self.maketable_definition()
      self.make_inserts()


   ### ADQL_JSON_PSQL.__init__()

   def debug(self,msg="",os=sys.stderr):             # ADQL_JSON_PSQL::debug()
      """Help with momentary debugging, file to fit."""
      print("ADQL_JSON_PSQL - %s " % msg, file=os)
      for key,value in self.__dict__.items():
         print("%20s = %s" % (key,value),file=os)

      return self

   ### ADQL_JSON_PSQL.debug()

   __ADQL_JSON_PSQL_debug = debug  # preserve our debug name if we're inherited

   def maketable_definition(self):                   # ADQL_JSON_PSQL::maketable_definition()
      """Given  the JSON structure, make the table definition.
      """

      for entry in self.json['metadata']:
         self.fieldnames.append(entry['name'])
         datatype = entry['datatype']
         if(datatype == 'long'):
            rettype = 'bigint'
         elif(datatype == 'double'):
            rettype = 'double precision'
         elif(datatype == 'float'):
            rettype = 'real'
         elif(datatype == 'int'):
            rettype = 'integer'
         elif(datatype == 'char' and entry['arraysize'] == '*'):
            rettype = 'text';
         else:
            rettype = 'text'
         self.fieldtypes.append(rettype)

      maxlen    = max(map(len,self.fieldnames))
      fmt       = """   {{:{:d}s}}   {{}}""".format(maxlen)
      outfields = []
      for f,t in zip(self.fieldnames,self.fieldtypes):
         outfields.append(fmt.format(f,t))  # make the field entry
      outlist = ',\n'.join(outfields)

      self.createstmt = ADQL_JSON_PSQL.table_declaration.format(self.tablename,outlist)

      return self

   ### ADQL_JSON_PSQL.maketable_definition()

   def make_inserts(self):                           # ADQL_JSON_PSQL::make_inserts()
      """Given the JSON dictionary, make insert statement"""
      insertfields    = ','.join(self.fieldnames)
      self.insertstmt = ADQL_JSON_PSQL.insert_statement.format(self.tablename,insertfields)
      self.insert()
      return self

   ### ADQL_JSON_PSQL.maketable_definition()

   def log_error(self,line,field,value,dtype):       # ADQL_JSON_PSQL::log_error()
      """Log the errors and return the string 'NULL'
      """
      self.errors,append("{} {} {} {}".format(line,field,value,dtype))
      return 'NULL'

   ### ADQL_JSON_PSQL.log_error()

   def sanity_check_data(self,line,field,value,dtype): # ADQL_JSON_PSQL.sanity_check_data()
      """Given a v and a type, sanity check it. Turn insane values
         into null, accumulate errors TODO
      """
      ret = 'NULL'
      if(dtype   == 'bigint' and type(value) is  type(1)):
         ret = '{}'.format(value)
      elif(dtype == 'double precision' and  type(1.0)):
         ret = '{}'.format(value)
      elif(dtype == 'real' and  type(float)):
         ret = '{}'.format(value)
      elif(dtype == 'integer' and type(value) is  type(1)):
         ret = '{}'.format(value)
      elif(dtype == 'text'):
         value = ADQL_JSON_PSQL.fixquotes.sub('',value)
         ret = "'{}'".format(value)
      else:
         self.log_errors.append(line,field,value,dtype)
         ret = self.errors(line,field,value,dtype)

      return ret

   ### ADQL_JSON_PSQL.sanity_check_data()

   def insert(self):                                 # ADQL_JSON_PSQL::insert()
      """Given the db description, connect to db,
      create the table, and make and insert the values
      """
      valuetext = []
      for line,rawline in enumerate(self.json['data']):  # it is an array of array's, line is []
         for i,l in enumerate(rawline):
            if(type(l) == type('str')):
               rawline[i] = ADQL_JSON_PSQL.fixnulls.sub('NULL',l)
         newline = []
         for field,z in enumerate(zip(rawline,self.fieldtypes)):  # field types are psql now
            v,t = z
            newline.append(self.sanity_check_data(line,field,v,t))
         valuetext.append("( {} )".format(','.join(newline)))
      # make the insert clause
      self.insertquery = self.insertstmt + '\n' + ',\n'.join(valuetext) + ';\n'

      return self
   
   ### ADQL_JSON_PSQL.insert()

   def db_load(self):                                # # ADQL_JSON_PSQL::db_load()
      """Establish the connection, and write the create and insert
         clauses into the db. Called of the -c option was used, by the
         classes manager.
      """

      try:
         conn   = psycopg2.connect(**self.db_description) #  dict of keyword/values.
      except Exception as e:
         print("ADQL_JSON_PSQL insert error",e,file=sys.stderr)
      else:
         try:
            cursor = conn.cursor()
         except Exception as e:
            print("ADQL_JSON_PSQL Create Cursor error {}".format(self.tablename))
         else:
            # Have the connection and a successful cursor
            try:
               cursor.execute(self.createstmt)
            except Exception as e:
               print("ADQL_JSON_PSQL Create Table error {}".format(self.tablename),
                     self.createstmt,e,file=sys.stderr)
            else:
               try:
                  cursor.execute(self.insertquery)
               except Exception as e:
                  print("ADQL_JSON_PSQL Insert Clause error {}".format(self.tablename))
                  raise
               else:
                  conn.commit()  # success here
      finally:
         conn.close()

      return self

   ### ADQL_JSON_PSQL.db_load()

   def writepsqlfile(self):                          # ADQL_JSON_PSQL::writepsqlfile()
      """Write a file, using tablename. Called if the -w flag option
         used by the classes manager.
      """
      with open('json2psql_{}.psql'.format(self.tablename),'w') as f: # PDB-DEBUG
         f.write(self.createstmt)
         f.write(self.insertquery)

      return self
   
    ### ADQL_JSON_PSQL.writepsqlfile()

# class ADQL_JSON_PSQL

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
                   help="<bool>   Direct connect to db and write the data.")

   opts.add_option("-t", "--table", action="store", dest="table",
                   default=None,
                   help="<str>    Table name.")

   opts.add_option("-D", "--database", action="store", dest="database",
                   default=None,
                   help="<str>    Database name.")

   opts.add_option("--host", action="store", dest="host",
                   default="localhost",
                   help="<str>    host [localhost].")

   opts.add_option("--port", action="store", dest="port",
                   default="5432",
                   help="<str>    port address.")

   opts.add_option("-u", "--username", action="store", dest="username",
                   default= getpass.getuser(),
                   help="<str>    username, defaults to login id.")

   opts.add_option("-w", "--write", action="store_true", dest="writeflasg",
                   default=False,
                   help="<bool>   Write a sidefile json2psql_<tablename>,psql.")

   opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>   be verbose about work.")

   opts.add_option("-w", "--write", action="store", dest="write",
                   default=None,
                   help="<str>    output file name for \\i ....")

   (options, args) = opts.parse_args()

   ###################################################################
   #  Get the options local and formatted. Prep kwds for psycopg2
   #  Get the password too.
   ###################################################################
   username = options.username
   password = 'Pluto!!1290' # getpass.getpass("{}'s psql Acct Password: ".format(username))
   table    = options.table
   database = options.database
   host     = options.host
   port     = "{}".format(options.port)       # cast to string
   db_definition = { 'dbname'   : database,
                     'user'     : username,
                     'password' : password,
                     'host'     : host,
                     'port'     : port
                   }

   tablename = options.table
   for f in args:
      jdb = ADQL_JSON_PSQL('rawmilesfields',db_definition,f)
      if(options.create):
         jdb.db_load()
      if(options.write):
         jdb.writepsqlfile()
