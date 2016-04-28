Merging X-ray spectra
---------------------------


The HEASOFT/ftools/addspec commands adds background spectra counts
inconsistent with poisson statistic.

You can detect this problem by seeing the number of counts in the various
energy bins in the background spectrum. If they are 0,1,2,3,4, there is no 
problem, if they are 0,510,1020,1530 there file is incorrect.

The python script (python mergebkg.py filelist prefix) provides and 
executes the correct mathpha command to create the correct background file.

Also a patch for HEASOFT/ftools/addspec is provided.

Please cite Buchner+16 if you use these tools.



