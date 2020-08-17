#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ciaran Robb, Aberystwyth University

Credit to authors of all libraries imported and used here. 
Please consult their individual licenses for usage. 

I have annotated the use of most libs excluding numpy as it is so basic and 
consituent to the rest

"""

import numpy as np
import mahotas as mh
import gdal, os
from geospatial_learn.utilities import imangle, do_phasecong
from geospatial_learn.raster import array2raster, polygonize
from skimage.morphology import remove_small_objects
from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from shapely.geometry import box, LineString
from tqdm import tqdm
from skimage.draw import line

gdal.UseExceptions()
ogr.UseExceptions()

def _std_huff(inArray, outArray,  angl, valrange, interval, rgt):
    
    #############################From here################################
    ################# Direct lift of scikit-image demo ###################
    
    tested_angles = np.linspace(angl - np.deg2rad(valrange), 
                                angl + np.deg2rad(valrange), num=interval)

    hh, htheta, hd = hough_line(inArray, theta=tested_angles)
    origin = np.array((0, inArray.shape[1]))

    height, width = inArray.shape
    
    #############################To here################################
    
    # Shapely
    bbox = box(width, height, 0, 0)
    

    #############################From here################################ 
    ################# Direct lift of scikit-image demo ###################             
    # Here we use the skimage loop to draw a bw line into the image
    for _, angle, dist in tqdm(zip(*hough_line_peaks(hh, htheta, hd))):
    
        # here we obtain y extrema in our arbitrary coord system
        y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
    #############################To here################################        
        
        # shapely used to get the geometry         
        linestr = LineString([[origin[0], y0], [origin[1], y1]])
        
        in_coord= np.array(bbox.intersection(linestr).coords)
        
        coord = np.around(in_coord)
        
        # for readability sake
        x1 = int(coord[0][0])
        y1 = int(coord[0][1]) 
        x2 = int(coord[1][0])
        y2 = int(coord[1][1])
        
        if y1 == height:
            y1 = height-1
        if y2 == height:
            y2 = height-1
        if x1 == width:
            x1 = width-1
        if x2 == width:
            x2 = width-1
        
        #skimage
        cc, rr = line(x1, y1, x2, y2)
        
        outArray[rr, cc]=1
    

    return outArray

def cropseg(inRas, outShp, edge='canny', sigma=2, 
               thresh=None, ratio=2, n_orient=6, n_scale=5, hArray=True, vArray=True,
               valrange=1, interval=10, band=2,
               min_area=None):
    

        # Standard GDAL I/O fair######################
        inDataset = gdal.Open(inRas, gdal.GA_ReadOnly)


        rgt = inDataset.GetGeoTransform()
        
        pixel_res = rgt[1]
        
        ################################################
        
        
        empty = np.zeros((inDataset.RasterYSize, inDataset.RasterXSize), dtype=np.bool)
        
            
        tempIm = inDataset.GetRasterBand(band).ReadAsArray()
        
        angleD, angleV, bw = imangle(tempIm)
        
        # mahotas
        perim = mh.bwperim(bw)
        
        hi_t = thresh
        low_t = np.round((thresh / ratio), decimals=1)

        if edge == 'phase':
            #geospatial_learn which itself calls phasepack
            ph = do_phasecong(tempIm, low_t, hi_t, norient=n_orient, 
                               nscale=n_scale, sigma=sigma)
            
            ph[perim==1]=0
            
            if hArray is True:
                vArray = ph
            if hArray is True:
                hArray = ph
            del ph
           
        else: 

            inIm = tempIm.astype(np.float32)
            inIm[inIm==0]=np.nan 
        
            if hArray is True:
                #skimage
                hArray = canny(inIm, sigma=sigma, low_threshold=low_t,
                               high_threshold=hi_t)
            if vArray is True:
                #skimage
                vArray = canny(inIm, sigma=sigma, low_threshold=low_t,
                               high_threshold=hi_t)
            del inIm
                                  
        
            
        if hasattr(vArray, 'shape'):            
            empty =_std_huff(vArray, empty,  angleV, valrange, interval, rgt)
        if hasattr(hArray, 'shape'):
            empty =_std_huff(hArray, empty,  angleD, valrange, interval, rgt)          


        inv = np.invert(empty)
        inv[tempIm==0]=0
        if min_area != None:
            min_final = np.round(min_area/(pixel_res*pixel_res))
            if min_final <= 0:
                min_final=4
            #skimage
            remove_small_objects(inv, min_size=min_final, in_place=True)
        segRas=outShp[:-3]+"seg.tif"
        
        # geospatial-learn
        array2raster(inv, 1, inRas, segRas,  gdal.GDT_Int32)
        del tempIm, inv
        
        # geospatial-learn
        polygonize(segRas, outShp[:-4]+"_poly.shp", outField=None,  mask = True, band = 1)  