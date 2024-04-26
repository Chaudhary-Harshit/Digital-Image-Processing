import cv2
import numpy as np
from collections import deque
img = cv2.imread("Assignment2.jpg")   # Loading the Image

# Converting to HSV 
img1 = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# Initializing the visited arrays for Longest connected component
visit_white= np.zeros(((img.shape[0])+4,(img.shape[1])+4))
visit_black = np.zeros(((img.shape[0])+4,(img.shape[1])+4))



# Generating Binary Image wrt to the range from HSV Image
def hsi_to_binaryimg(img):
    image1 = img.copy()
    x = img.shape[0]
    y = img.shape[1]
    new_img = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            if( image1[i,j,2] < 200 and  60 < image1[i,j,1] < 75 and image1[i,j,0]< 28):
                new_img[i,j] = 255
            else:
                new_img[i,j] = 0
    return new_img 




# Adding Padding to the image for respective kernel size            
def padding(img,ker_size):
    pad_size= ker_size//2
    pad_img= np.zeros((img.shape[0]+(2*pad_size),img.shape[1]+(2*pad_size)))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pad_img[i+pad_size][j+pad_size]= img[i][j]

    return pad_img




# Function to be used in Dilation, returns 1 if any image pixel coincides with kernel and returns 0 otherwise
def hit(kernel,x,y,img):
    pad_size= kernel.shape[0]//2
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            if(kernel[i][j]==img[x + i  - pad_size][y + j - pad_size]):
                return 1

    return 0





# Function to be used in Erosion, returns 1 if all image pixel coincides with kernel and returns 0 otherwise
def fit(kernel,x,y,img):
    pad_size= kernel.shape[0]//2
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            if(kernel[i][j]!=img[x + i  - pad_size][y + j - pad_size]):
                return 0
                
    return 1




# Dilation --> If there is a hit, we assign 255 to the pixel for which hit is called, else 0 
def dilation(img,ker_size):
    kernel = np.full((ker_size, ker_size),255,np.uint8)
    pad_size = ker_size//2
    dilated_img = img.copy()
    for x in range(pad_size,img.shape[0] - pad_size):
        for y in range(pad_size,img.shape[1] - pad_size):
            if(hit(kernel,x,y,img)==1):
               dilated_img[x][y] = 255
            else:
                dilated_img [x][y] = 0
    return dilated_img 





# Erosion --> If there is no fit, we assign 0 to the pixel for which fit is called, else it remains same
def erosion(img,ker_size):
    kernel = np.full((ker_size, ker_size),255,np.uint8)
    pad_size = ker_size//2
    eroded_img = img.copy()
    for x in range(pad_size,img.shape[0] - pad_size):
        for y in range(pad_size,img.shape[1] - pad_size):
            if(fit(kernel,x,y,img) == 0):
                eroded_img [x][y] = 0
            
    return eroded_img 





# Takes AND of mask and original Image
# Assigns 255 (white) to all pixels that are black in binary Image (Mask) and the other pixels remain same
def Logical_AND(img1):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if(img1[i][j]==0):
                img[i][j][0] = 255
                img[i][j][1] = 255
                img[i][j][2] = 255
    return img  





# Returns 1 if the black pixel has already been visited
def check_visit_black(i,j):
        if visit_black[i][j]==1:
            return 1
        else:
            return 0




# Returns All the black neighbours out of 8 connected neighbours of a pixel
def connect_black(img,i,j):
        eight_neighbours=[]
        black_connected_neigbours=[]
        # We have used extension function, it is used to do multiple appends to a list at once
        eight_neighbours.extend([[i-1,j-1],[i-1,j],[i-1,j+1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]])

        for neigbour in eight_neighbours:
            if neigbour[0] in range(img.shape[0]) and neigbour[1] in range(img.shape[1]):
                x=neigbour[0]
                y=neigbour[1]
                if img[x][y]==0:
                    black_connected_neigbours.append([x,y])

        return black_connected_neigbours




# Finds the longest Black Connected Component
def lcc_black(dil_img):
    
    de= deque()
    longest_connected_component=[]
    list_longest_connected_components=[]


    for i in range(2,dil_img.shape[0]-2):
        for j in range(2,dil_img.shape[1]-2):
            if dil_img[i][j]==0:
                check= check_visit_black(i,j)
                if check==0:
                    # Appending the coordinate of the pixel in the queue
                    de.append((i,j))

                    # Looping while Queue is not empty 
                    while len(de)!=0:

                        # popleft() removes the element from the beginning of the dequeue
                        popped_pixel=de.popleft()
                        longest_connected_component.append([popped_pixel[0],popped_pixel[1]])
                        checker_of_popped_pixel=check_visit_black(popped_pixel[0],popped_pixel[1])


                        if checker_of_popped_pixel==0:
                            connected_black_neighbours=connect_black(dil_img,popped_pixel[0],popped_pixel[1])
                            visit_black[popped_pixel[0]][popped_pixel[1]]=1

                            for i in range(len(connected_black_neighbours)):
                                de.append((connected_black_neighbours[i][0],connected_black_neighbours[i][1]))
        
                    list_longest_connected_components.append(longest_connected_component)
                    longest_connected_component=[]    
                else:
                    pass
    
    # Finding the longest Connected Component from the array of Connected Components
    lcc=list_longest_connected_components[0]

    for i in range(len(list_longest_connected_components)):
        
        if len(list_longest_connected_components[i])>len(lcc):
            lcc=list_longest_connected_components[i]

    # Using the coordinates of the longest connected component, generating the binary image of the lcc
    lcc_binary_image = np.full((dil_img.shape[0],dil_img.shape[1]),255,np.uint8)

    for pixel in lcc:
        lcc_binary_image[pixel[0]][pixel[1]]=0
    return lcc_binary_image



# Returns 1 if the white pixel has already been visited
def check_visit_white(i,j):
        if visit_white[i][j]==1:
            return 1
        else:
            return 0




# Returns All the black neighbours out of 8 connected neighbours of a pixel
def connect_white(img,i,j):
        eight_neighbours=[]
        white_connected_neigbours=[]
        eight_neighbours.extend([[i-1,j-1],[i-1,j],[i-1,j+1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]])

        for neighbour in eight_neighbours:
            if neighbour[0] in range(img.shape[0]) and neighbour[1] in range(img.shape[1]):
                x=neighbour[0]
                y=neighbour[1]
                if img[x][y]==255:
                    white_connected_neigbours.append([x,y])

        return white_connected_neigbours



# Returns the Binary Image of the White longest connected component
def lcc_white(dil_img):
    
    de= deque()
    connected_component=[]
    list_of_connected_component=[]

    for i in range(2,dil_img.shape[0]-2):
        for j in range(2,dil_img.shape[1]-2):
            if dil_img[i][j]==255:
                check= check_visit_white(i,j)
                if check==0:
                    de.append((i,j))
                    while len(de)!=0:
                        popped_pixel=de.popleft()
                        connected_component.append([popped_pixel[0],popped_pixel[1]])
                        checker_of_popped_pixel=check_visit_white(popped_pixel[0],popped_pixel[1])

                        if checker_of_popped_pixel==0:
                            connected_white_neighbours=connect_white(dil_img,popped_pixel[0],popped_pixel[1])
                            visit_white[popped_pixel[0]][popped_pixel[1]]=1

                            for i in range(len(connected_white_neighbours)):
                                de.append((connected_white_neighbours[i][0],connected_white_neighbours[i][1]))
        
                    list_of_connected_component.append(connected_component)
                    connected_component=[]    
                else:
                    pass

    lcc=list_of_connected_component[0]
    for i in range(len(list_of_connected_component)):

        if len(list_of_connected_component[i])>len(lcc):
            lcc=list_of_connected_component[i]
    lcc_binaryimg= np.zeros((dil_img.shape[0],dil_img.shape[1]))

    for pixel in lcc:
        lcc_binaryimg[pixel[0]][pixel[1]]=255
    return lcc_binaryimg








Binary_img = hsi_to_binaryimg(img1)

#Added padding for kernel 5 x 5 
pad_img = padding(Binary_img,5)

dil_img = dilation(pad_img,5)
black_lcc = lcc_black(dil_img)
white_lcc = lcc_white(black_lcc)

# Opening
eros1 = erosion(white_lcc,3)
dil1 = dilation(eros1,7)


dil2 = dilation(dil1,7)
eros2 = erosion(dil2,7)
eros3 = erosion(eros2,7)

final_elephant = Logical_AND(eros3)


cv2.imshow('Extracted Colour Elephant',final_elephant)

cv2.waitKey(0)



cv2.destroyAllWindows()