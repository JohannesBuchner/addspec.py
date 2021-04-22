Summing/Merging/Adding X-ray point source spectra
==================================================

The HEASOFT/ftools/addspec commands adds background spectra counts
inconsistent with poisson statistic.

You can detect this problem by seeing the number of counts in the various
energy bins in the background spectrum. If they are 0,1,2,3,4, there is no 
problem, if they are 0,510,1020,1530 the file is incorrect.

The python script (python addspec.py filelist prefix) provides and 
executes the correct mathpha command to create the correct background file.

Improvements are welcome.

Usage
------

::

	$ addspec.py prefix file1.pha file2.pha file3.pha

or::

	$ addspec.py prefix @src.txt

where src.txt contains the filenames (one line each).

Licence
--------

MIT
