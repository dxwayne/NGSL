============
Introduction
============

This project sought out suitable FITS spectra from the World Wide Web
to support absolute calibration of small telescope science
spectra. Recently the Uvex project is taking small telescope
spectroscopy into the very near UV -- ~ 3200 angstroms.

The Next Generation Spectral Library Version 2, contains spectra taken
with the Hubble Space Telescope STIS instrument.  It has its issues,
but the resolution meets the R 1000 instruments, and its range covers
0.2 to 1 microns. Ideal for the UVEX instrument.

These data are not extinction corrected. They represent zero-point
data at the altitude of Hubble. They have no telluric contamination.

This project downloaded the FITS table files, converted them to
**.dat** files.  It created a PostgreSQL database with the headers. It
used queries to build additional tables with SIMBAD information etc.
A tulleric table is included.

Other information is included as well.

In addition to the NGSL (stis) data, a quick survey of other libraries
was made, and these data cataloged as well in the development image.

Here we release the a database with the results of the conversion of
the NGSL V2 files together with SIMBAD data.

During the production of the data base Python utilities were created
to assist with the process.

Further examination of TOPCAT's features reveal that it is quite
possible to build the PostgreSQL database's tables directly based
on TAP (ADQL) queries with joins. TOPCAT has come a long way in the
past few years.






.. csv-table:: **File List**
   :header: "File", "Description"
   :widths: 30, 90

   "__init__.py","Python cruft"
   "AlbersExampleTable.py","Emerging ATM data"
   "Chainti.py","Test link to Chainty Line Data"
   "GAO_VOTables.py","Hack for VO tables"
   "bessel1983.py","Convert spectral source data"
   "calobs2dat","Convert spectral source data"
   "fits1d2dat","Work with 1D FITS file (emerging)"
   "fits2psqlraw","Convert multi-HDU to psql using jsonb"
   "jacobi2dat","Convert spectral source data"
   "json2psql","Given json data from web,  hack for psql"
   "khan2dat","Convert spectral source data"
   "miles2psql.py","Convert spectral source data"
   "stis2dat","Convert spectral source data"
