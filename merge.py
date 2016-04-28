import numpy
import sys
import astropy.io.fits as pyfits
cts = 0
bcts = 0
r = 0
a = 0
totexposure = 0
totbexposure = 0

for filename in open(sys.argv[1]):
	f = pyfits.open(filename.rstrip())
	backscal = f[1].header['BACKSCAL']
	areascal = f[1].header['AREASCAL']
	exposure = f[1].header['EXPOSURE']
	#print exposure, areascal, backscal
	totexposure = totexposure + exposure * areascal * backscal
	
	cts = cts + f[1].data['COUNTS']
	
	backfile = f[1].header['BACKFILE']
	fb = pyfits.open(backfile)
	#print fb
	bcts = bcts + fb[1].data['COUNTS']
	bbackscal = fb[1].header['BACKSCAL']
	bareascal = fb[1].header['AREASCAL']
	bexposure = fb[1].header['EXPOSURE']
	totbexposure = totbexposure + bexposure * bareascal * bbackscal

	respfile = f[1].header['RESPFILE']
	fr = pyfits.open(respfile)
	#print fr, fr[1].name, fr[2].name
	print fr['MATRIX'].data['MATRIX'].shape, numpy.shape(r), exposure * areascal * backscal
	print (fr['MATRIX'].data['MATRIX'] * exposure * areascal * backscal)
	r = r + fr['MATRIX'].data['MATRIX'] * exposure * areascal * backscal
	ancrfile = f[1].header['ANCRFILE']
	fa = pyfits.open(ancrfile)
	#print fa, fa['SPECRESP'].name
	#print fa['SPECRESP'].data.dtype
	a = a + fa['SPECRESP'].data['SPECRESP'] * exposure * areascal * backscal

outprefix = sys.argv[2]
# update values of first file and save to merged file	
f[1].header['BACKSCAL'] = 1.
f[1].header['AREASCAL'] = 1.
f[1].header['EXPOSURE'] = totexposure
f[1].data['COUNTS'] = cts
f[1].header['BACKFILE'] = outprefix + '_bk.pi'
f[1].header['RESPFILE'] = outprefix + '.rmf'
f[1].header['ANCRFILE'] = outprefix + '.arf'
f.writeto(outprefix + '.pi', clobber=True)

fb[1].header['BACKSCAL'] = 1.
fb[1].header['AREASCAL'] = 1.
fb[1].header['EXPOSURE'] = totbexposure
fb[1].data['COUNTS'] = bcts
fb[1].header['RESPFILE'] = outprefix + '.rmf'
fb[1].header['ANCRFILE'] = outprefix + '.arf'
f.writeto(outprefix + '_bk.pi', clobber=True)

fr['MATRIX'].data['MATRIX'] = r / totexposure
fr.writeto(outprefix + '.rmf', clobber=True)
fa['SPECRESP'].data['SPECRESP'] = a / totexposure
fa.writeto(outprefix + '.arf', clobber=True)



