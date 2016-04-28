import numpy
import sys
import astropy.io.fits as pyfits
cts = 0
bcts = 0
r = 0
a = 0
totexposure = 0
totbexposure = 0
outprefix = sys.argv[2]

backfiles = []
totareascal = 0
totbackscal = 0
for filename in open(sys.argv[1]):
	f = pyfits.open(filename.rstrip())
	backscal = f[1].header['BACKSCAL']
	areascal = f[1].header['AREASCAL']
	exposure = f[1].header['EXPOSURE']
	#print exposure, areascal, backscal
	totexposure = totexposure + exposure# * areascal * backscal
	totareascal = totareascal + areascal
	totbackscal = totbackscal + backscal
	
	backfile = f[1].header['BACKFILE']
	fb = pyfits.open(backfile)
	#print fb
	bcts = bcts + fb[1].data['COUNTS']
	bbackscal = fb[1].header['BACKSCAL']
	bareascal = fb[1].header['AREASCAL']
	bexposure = fb[1].header['EXPOSURE']
	totbexposure = totbexposure + bexposure * bareascal / areascal * bbackscal / backscal
	
	print filename.strip(), backfile
	print '    exposure: %.1f %.1f' % (exposure, bexposure)
	print '    areascal: %.1f %.1f' % (areascal, bareascal)
	print '    backscal: %.6f %.6f' % (backscal, bbackscal)
	weight = backscal / bbackscal * 1000
	print '    addspec weight: %.3f' % (weight)
	print '    weighted exposure: %.3f' % (bexposure * bareascal / areascal * bbackscal / backscal)
	backfiles.append(backfile)

#totbexposure = totbexposure * 10000
print 'total exposure: %.1f (src)' % totexposure
print 'total exposure: %.1f (bkg)' % totbexposure

cmd = ["mathpha", "expr=%s" % '+'.join(backfiles), "outfil=%s.bak" % outprefix, "units=C", "exposure=%.2f" % totbexposure,
	"properr=NO", "errmeth=POISS-0", "areascal=NULL", "ncomments=2", "comment1=Created_by_mergebkg.py_from_Johannes_Buchner", "comment2=Because_addspec_sucks", "chatter=5"]
print ' '.join(cmd) #.replace('(', '\(').replace(')', '\)')
import subprocess
p = subprocess.Popen(cmd)
p.wait()

