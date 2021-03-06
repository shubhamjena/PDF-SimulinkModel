# -*- coding: utf-8 -*-
"""
Created on Thu May  7 08:45:18 2020

@author: Shaun Zacharia
"""


import cv2
import numpy as np
import os

# reading the image
print('reading image')
img = cv2.imread('untitled/0.jpg', 1)
print('image read')

# convert the image to grayscale
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
# convert the grayscale image to binary image
ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

def fill(image, save = True):
    """
    Parameters
    ----------
    image : Takes in a binary thresholded image
        Will also work with colour images, but the results won't be as good.
        
    save : Boolean
        If True, it will save the image in jpg format with the name 'filled.jpg'
        in the location of the working directory

    Returns
    -------
    mask : The array version of the filled image
    Creates image with all the enclosed spaces filled
    """
    # filling all enclosed areas
    h, w = image.shape[:2]
    seed = (w//2,h//2)
    mask = np.zeros((h+2,w+2),np.uint8)
    floodflags = 4
    floodflags |= cv2.FLOODFILL_MASK_ONLY
    floodflags |= (255 << 8)
    num,thresh,mask,rect = cv2.floodFill(image, mask, seed, (255,0,0), (10,)*3,
                                         (10,)*3, floodflags)
    
    # saving the mask
    if save:
        cv2.imwrite("filled.jpg", mask)
    return mask


filled = fill(thresh)
print('image filled')


def removeLines(image, save = True):
    """
    Parameters
    ----------
    image : ndarray
        The input image from which lines are to be eroded.
    save : Boolean, optional
        If true, it saves the no line image in the working directory with the
        name 'no lines.jpg'. The default is False.

    Returns
    -------
    no_line : ndarray
        Performs morphological dilation to cause the lines to get eroded.
    """
    
    kernel = np.ones((5, 5), np.uint8)
    
    # morphological operation to remove the lines
    no_line = cv2.dilate(filled, kernel, iterations=3)
    if save:
        cv2.imwrite("no lines.jpg", no_line)
    return no_line


no_line = removeLines(filled, save = True)
print('lines removed')

def getEnclosed(no_line, image, output_size = 120, save = True):
    """
    Parameters
    ----------
    no_line : ndarray
        Takes the image with eroded lines as input, has to be binary image.
    image : ndarray
        Takes the image from which segmented parts should be cropped out.
        Will work best if binary thresholded image is given as argument.
    output_size : int, optional
        All the cropped images will be padded to become of this size, 
        its value should be greater than the width/height of each Region 
        of Interest. The default is 120.
    save : Bool, optional
        If true, it saves each region of interest in the working directory
        with the nameing convention 'ROI_i.jpg', where i is the i'th image.
        The default is False.

    Returns
    -------
    regions : ndarray of shape (num_regions, output_size, output_size)
        Contains each region of interest in array format.

    """
    # n is amount by which to widen area since we get eroded image
    # 11 = 5 + (5-2)*(no. of iterations)
    n = 11
    ROI_number = 0
    original = image.copy()
    
    # getting contours in the image, 255-no_line so that base is black
    cnts = cv2.findContours(255-no_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    # creating empty stack in which all segmented images will be stored
    regions = np.zeros((len(cnts), output_size, output_size))
    
    for i, c in enumerate(cnts):
        x,y,w,h = cv2.boundingRect(c)
        #cv2.rectangle(image, (x-n, y-n), (x + w + n, y + h + n), (36,255,12), 2)
        ROI = original[y-n : y+h+n, x-n : x+w+n]
        if save:
            cv2.imwrite('enclosed\ROI_{}.jpg'.format(ROI_number), ROI)
        
        ww = hh = output_size
        ht, wd = ROI.shape
        # compute center offset
        xx = (ww - wd) // 2
        yy = (hh - ht) // 2
        regions[i, yy:yy+ht, xx:xx+wd] = ROI
        ROI_number += 1
        
    return regions


regions = getEnclosed(no_line, thresh, save = True)
print('enclosed')