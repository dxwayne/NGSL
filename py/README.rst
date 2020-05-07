README
======

This package is a tool suite and library to support working
with small telescope spectra observations.

NGSL is a collection of tabular data of the Next Generation Spectral
Library and useful for small telescope scientists to perform
reasonably accurate calibration of stellar spectra.


Contents
--------

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

Status
------

These are programs and modules that share code and data.
Here we are cleaning up the hacks and making a Python module
for general support.

Most code here needs to be enhanced for Sphinx documentation.
