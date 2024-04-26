import cv2
import numpy as np

diagonal_coordinates = []
cropped_image= []
img = cv2.imread('./images/lena_color.tif',0)
copy=img

def Nearest_Neighbour_Replication(img,factor):
  img=np.repeat(img,factor,axis=1)   # Repeats every column by the factor times
  img= np.repeat(img,factor,axis=0)   # Repeats every row by the factor times
  return img

def click(event,x,y,flags,param):    # Mouse Handler
  global diagonal_coordinates,cropped_image

  if event==cv2.EVENT_LBUTTONDOWN:
    diagonal_coordinates=[[x,y]]

  elif event==cv2.EVENT_LBUTTONUP:
    diagonal_coordinates.append([x,y])

  cv2.rectangle(img,diagonal_coordinates[0],diagonal_coordinates[1],(0,255,0),2)

  cropped_image=copy[diagonal_coordinates[0][1]:diagonal_coordinates[1][1],diagonal_coordinates[0][0]:diagonal_coordinates[1][0]]    # Recognises the Selected area by the mouse
  cropped_image=Nearest_Neighbour_Replication(cropped_image,2)    # Executes NNI on the selected Area
  cv2.imshow('image1',cropped_image)
  cv2.imshow('image',img)


cv2.imshow('image',img)
cv2.setMouseCallback('image',click)  # Calls the Click Function
cv2.waitKey(0)
cv2.destroyWindow('image')