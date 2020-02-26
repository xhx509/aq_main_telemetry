# routine to provide model and climatologic temperature given lat,lon,depth, and time at command line
# To run this routine, for example, in Python3 type: 
#     run all_models_test 41.9 -70.25 99999 2019 8 15 0 0
# for Mass Bay bottom temps near mid-night (GMT) at the start of Aug 15th, 2019 
# Author JiM borrowing many functions/modules of students
# Note: hardcoded directory for climatology file storage
# Note: modules needed in this directory include those for gomofs,doppio,fvcom,conversions, and maybe others?

import sys
import pandas as pd
import numpy as np
import gomofs_modules
import doppio_modules
import fvcom_modules
from datetime import datetime as dt

#HARDCODES ############
# Gets imput from terminal
lat=float(sys.argv[1])
lon=float(sys.argv[2])
depth=int(sys.argv[3])#99999 for bottom
datet=dt(int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]),0)
clim_files_directory='/net/data5/jmanning/clim/'
#####################

# get GOMOFS
try:
    t=gomofs_modules.get_gomofs(datet,lat,lon,depth)
    print('gomofs = ','%.3f' % t)
except:
    print('gomofs not available?')

# get DOPPIO
try:
    t=doppio_modules.get_doppio(lat,lon,depth,datet,'temperature')
    print('doppio = ','%.3f' % t)
except:
    print('doppio not available?')

# get FVCOM
try:
    url=fvcom_modules.get_FVCOM_url(datet)
    t=fvcom_modules.get_FVCOM_temp(url,lat,lon,datet,depth)# 
    print('fvcom =','%.3f' % t)
except:
    print('fvcom not available?')

# get CLIM
dflat=pd.read_csv(clim_files_directory+'LatGrid.csv',header=None)
dflon=pd.read_csv(clim_files_directory+'LonGrid.csv',header=None)
bt=pd.read_csv(clim_files_directory+'Bottom_Temperature/BT_'+datet.strftime('%j').lstrip('0')+'.csv',header=None) # gets bottom temp for this day of year with leading zero removed
latall=np.array(dflat[0])   # gets the first col (35 to 45)
lonall=np.array(dflon.loc[0])# gets the first row (-75 to -65) changed "ix to "loc" in Feb 2020
idlat = np.abs(latall - lat).argmin()# finds the nearest lat
idlon = np.abs(lonall - lon).argmin()# finds the nearest lon
print('bottom clim =','%.3f' % bt[idlon][idlat])
