# routine to test "getfvcom" function
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil import parser
import pandas as pd
import numpy as np
import netCDF4
import sys
from conversions import c2f,dd2dm

def nearlonlat(lon,lat,lonp,latp): # needed for the next function get_FVCOM_bottom_temp
    """
    i=nearlonlat(lon,lat,lonp,latp) change
    find the closest node in the array (lon,lat) to a point (lonp,latp)
    input:
        lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
        lonp,latp - point on a sphere
        output:
            i - index of the closest node
            For coordinates on a plane use function nearxy           
            Vitalii Sheremet, FATE Project  
    """
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    i=np.argmin(dist2)
    return i

def get_FVCOM_url(dtime):
    """dtime: the formate of time is datetime"""
    # get fvcom url based on time wanted
    if (dtime-dt.now())>td(days=-2):
        url='http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc' 
    elif dtime>=dt(2016,7,1):
        url='http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM/2019/gom4_201907.nc'
        url=url.replace('201907',dtime.strftime('%Y%m'))
        url=url.replace('2019',dtime.strftime('%Y'))
    elif dtime<=dt(2016,1,1):
        url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
    else:
        url=np.nan
    return url

def get_FVCOM_temp(urlfvcom,lati,loni,dtime,depth): # gets modeled temp using GOM3 forecast
        '''
        Taken primarily from Rich's blog at: http://rsignell-usgs.github.io/blog/blog/2014/01/08/fvcom/ on July 30, 2018
        where lati and loni are the position of interest, dtime is the datetime, and depth is "99999" for bottom
        '''
        nc = netCDF4.Dataset(urlfvcom).variables
        #first find the index of the grid 
        lat = nc['lat'][:]
        lon = nc['lon'][:]
        inode = nearlonlat(lon,lat,loni,lati)
        #second find the index of time
        time_var = nc['time']
        itime = netCDF4.date2index(dtime,time_var,select='nearest')# where startime in datetime
        # figure out layer from depth
        w_depth=nc['h'][inode]
        if depth==99999: # for bottom
            layer=-1
        else:
            layer=int(round(depth/w_depth*45.))
        return nc['temp'][itime,layer,inode]

