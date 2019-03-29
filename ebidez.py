#############################################################
# EBIDEZ
# 
# An attempt to identify eclipsing binaries 
# in TESS light curve data.
#
# A 2D histogram is generated of the lightcurve
# along time and flux directions
# the shift of the mode of the flux in time
# is compared to a limit value (hlim)
#
# if the number of peaks is between nlim and plim
# the light curve may contain an eclipsing binary
#
# written by S. Eggl and M. Kudryashova 20190329
#############################################################

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import glob
import os

### PARAMETERS TO PLAY WITH
### MODE PEAK / DROUGHT FILTERS
#minimum number of mode excursions (eclipses) for detection
nlim=5
# bin limit for mode movement to identify eclipses 
hlim=20
# upper number of mode excursions (eclipses) for detection
plim=50

### FLUX FILTERS
#flux min
fmin=1500
# minimum distance between min flux and max flux in percent
dfmin=10

### HISTOGRAM 
#time bins
tbins=200
#flux bins 
fbins=50

### TESS INPUT DATA
fluxtype="PDCSAP_FLUX"
path_to_lcs='/data/epyc/data/tess/sector003/*.fits'

### DON'T TOUCH ANYTHING BELOW HERE
dfminp=dfmin/100.
j=0
for i in glob.glob(path_to_lcs):
	try:
		hdu_list = fits.open(i)
	
		image_data = hdu_list[1].data
	
		dat=image_data[~np.isnan(image_data[fluxtype])]
		
		if((dat[fluxtype].max()>fmin) & (((dat[fluxtype].max()-dat[fluxtype].min())/dat[fluxtype].mean())>dfminp)):

			[hist,xbins,ybins]=np.histogram2d(dat["TIME"],dat[fluxtype], bins=[tbins,fbins], range=None)
	
			hmax=np.argmax(hist[:,:],1)
	
			npeaks=len(np.where((hmax<hlim) & (hmax > 0))[0])

			if ((npeaks>nlim)&(npeaks<plim)):
### PLOTTING			
				plt.figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
				plt.plot(image_data["TIME"],image_data[fluxtype],',')
				plt.xlabel('TESS epoch [days]')
				plt.ylabel(r'FLUX [e$^-$/s]')
				plt.title(i[31:-5])
				plt.savefig(('eb_%d.png'%j), dpi=150, facecolor='w', edgecolor='w', format='png')
				plt.close()
				j=j+1

	except:
		print('could not read',i)
		
