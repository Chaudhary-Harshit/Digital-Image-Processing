import cv2
import numpy as np

img = cv2.imread('./images/lena_color.tif')
print('Size of Shape before Shrinking ',img.shape)

def shrinking(img):
    new_image= np.delete(img,np.s_[0:img.shape[1]:2],axis=1)  # Alternate Columns are getting deleted
    new_image= np.delete(new_image,np.s_[0:img.shape[0]:2],axis=0)   # Alternate rows are getting deleted
    print('Size of Shape After Shrinking ',new_image.shape)
    cv2.imshow('image',new_image)

shrinking(img)
cv2.waitKey(0)             
cv2.destroyWindow('image')

''' 
    We have used np.delete function from Numpy library which takes three arguments 
        1.The Image 2. np.s Function 3.Axis[defines performed task to be on row/column]
    The np.s function uses slicing where it returns index list of every second column/row for the 
    delete function to use.
'''