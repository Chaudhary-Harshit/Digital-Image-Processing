import cv2
import numpy as np

def to_binary(n,bit):   # Returns the required bit of the number n in binary
  s=""
  while(n>0):
    x=n%2
    s+=str(x)
    n=n//2
    
  if len(s)<8:
    while(len(s)!=8):
      s+='0'

  return int(s[bit-1])


def Reconstruction(a,planes): #Reconstructs the image uding the planes in planes array(as a parameter)
  new_image=np.zeros((a.shape[0],a.shape[1]),dtype=np.uint8) # a is the new image
  for plane in planes:
    for i in range(a.shape[0]):
      for j in range(a.shape[1]):
        new_image[i][j]+=(to_binary(a[i][j],plane))*2**(plane-1)

  cv2.imshow(f'reconstruct_by_plane_{planes}',new_image)


img = cv2.imread('./images/lena_color.tif',0)
for i in range(3):
  if(i==0):
    Reconstruction(img,[8,7])
    cv2.waitKey(2000)
    cv2.destroyWindow('reconstruct_by_plane_[8,7]')
  elif(i==1):
    Reconstruction(img,[8,7,6])
    cv2.waitKey(2000)
    cv2.destroyWindow(f'reconstruct_by_plane_[8,7,6]')
  else:
    Reconstruction(img,[8,7,6,5])
    cv2.waitKey(2000)
    cv2.destroyWindow(f'reconstruct_by_plane_[8,7,6,5]')