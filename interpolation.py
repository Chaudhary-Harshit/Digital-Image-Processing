import cv2
import numpy as np

def inter (original,m):
  row_counter=0
  column_counter=0
  x=(original.shape[0])*m
  y= (original.shape[1])*m
  new = np.zeros((x,y))
  for i in range(0,x,m):
    column_counter=0
    for j in range(0,y,m):
      new[i][j]=original[row_counter][column_counter]
      column_counter+=1
    row_counter+=1

  for i in range(0,x,m):
    for j in range(1,y,m):
      if(j==y-1):
        new[i][j] = new[i][j-1]/2
      else:
        new[i][j]= (new[i][j+1]+new[i][j-1])/2
  
  for i in range(1,x,m):
    for j in range(0,y,m):
      if(i==x-1):
        new[i][j]= new[i-1][j]/2
      else:
        new[i][j] = (new[i-1][j] + new[i+1][j])/2
      
  for i in range(1,x,m):
    for j in range(1,y,m):
      if(j==y-1 and i!=x-1):
        new[i][j]= (new[i-1][j]+new[i+1][j]+new[i][j-1])/3
      elif(i==x-1 and j!=y-1):
        new[i][j]= (new[i-1][j]+new[i][j+1]+new[i][j-1])/3
      elif(i==x-1 and j==y-1):
        new[i][j]= (new[i-1][j]+new[i][j-1])/2
      else:
        new[i][j]= (new[i-1][j]+new[i+1][j]+new[i][j-1]+new[i][j+1])/4

  new=np.asarray(new,dtype=np.uint8) 
  return new
 

diagonal_coordinates=[]
cropped_image=[]
img= cv2.imread('./images/lena_color.tif',0)
copy=img

def click(event,x,y,flags,param): # Mouse Handler
  global diagonal_coordinates,l

  if event==cv2.EVENT_LBUTTONDOWN:
    diagonal_coordinates=[[x,y]]

  elif event==cv2.EVENT_LBUTTONUP:
    diagonal_coordinates.append([x,y])

  cv2.rectangle(img,diagonal_coordinates[0],diagonal_coordinates[1],(0,255,0),2)
  print(diagonal_coordinates)

  cropped_image=copy[diagonal_coordinates[0][1]:diagonal_coordinates[1][1],diagonal_coordinates[0][0]:diagonal_coordinates[1][0]]
  cropped_image=inter(cropped_image,2)
  cv2.imshow('image1',cropped_image)
  cv2.imshow('image',img)

  
cv2.imshow('image',img)
cv2.setMouseCallback('image',click)
# print(img)
cv2.waitKey(0)
cv2.destroyAllWindows()

