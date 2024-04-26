import cv2
import numpy as np

def to_binary(n,bit):  # Returns the required bit of the number n in binary
  s=""
  while(n>0):
    x=n%2
    s+=str(x)
    n=n//2
    
  if len(s)<8:
    while(len(s)!=8):
      s+='0'

  return int(s[bit-1])


def plane_slicing(a,plane):                            # Shows nth bit plane image
  new_image=np.zeros((a.shape[0],a.shape[1]),dtype=np.uint8)  # a is the original image
  for i in range(a.shape[0]):
    for j in range(a.shape[1]):
      new_image[i][j]=(to_binary(a[i][j],plane))*(255)

  cv2.imshow(f'bit_plane_{plane}',new_image)


img = cv2.imread('./images/lena_color.tif',0)
for i in range(1,9):       
    plane_slicing(img,i)
    cv2.waitKey(2000)
    cv2.destroyWindow(f'bit_plane_{i}')


# The output will show plane 1 to 8 in a row with a delay of 2 seconds between each.
# The Image name will be the current Bit plane Iamge
 