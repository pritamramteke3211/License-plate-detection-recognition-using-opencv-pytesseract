import cv2
import imutils  # to resize our images
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#now to read the image file
pic = cv2.imread('5.jpg')

#we will resize and standardise our image to 500
image = imutils.resize(pic, width = 500)

# we will display original image when it will start finding
cv2.imshow('Original Image',image)  #where original image is the name of window /// you can give suitable name
cv2.waitKey(0) # till i press anything it will not execute further

# Now we will convert image to gray scale
# why we do is because it will reduce the dimension , also reduces complexity of image
# and yeah there are few algorithms like canny, etc which only works on grayscale images

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Scale Image',gray)
cv2.waitKey(0)

# now we will reduce noise from our image and make it smooth
smooth = cv2.bilateralFilter(gray, 11,17,17)
cv2.imshow('Smoother Image',smooth)
cv2.waitKey(0)


# so now will find the edges of images
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("Canny edge",edged)
cv2.waitKey(0)


#now we will find the contours based on the images
cnts , new = cv2.findContours(edged.copy(),cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)
#ok so here cnts is contours which means that it is like the curve joining all the contior points
# new is heirarchy-relationship
# RETR_LIST - it retrives all the contours but doen't create any parent-child relationship
# CHAIN_APPROX_SIMPLE - it removes all the redundant points and compress the contour by saving memory


# we will create a copy of our original image to draw all the contours
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0,255,0),3)  # this values are fixed  ## to draw all the contours in an image
cv2.imshow("Canny after contouring",image1)
cv2.waitKey()

#now we don't want all the coutours we are intrested only in number plate
#but can't directly locate that so we will sort them on the basis of their areas
#we will select those area which are maximum so we will select top 30 areas
#but it will give sorted list as in order of min to maximum
# so for that we will reverse the order of sorting

cnts = sorted(cnts,key= cv2.contourArea,reverse=True)[:30]
NumberPlateCount = None

#because currently we don't have any contour or you can say it will show how many number plates are their in image

#to draw top 30 contours we will make copy of original image and use
# use because we don't want to edit anything in our original image

image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("TOP 30 Contours",image2)
cv2.waitKey(0)

#now we will run a for loop on our contours to find the best possible contour of our expectes number plate
count = 0
name = 1     #name of our image(cropped image)

for i in cnts:
    perimeter = cv2.arcLength(i, True)
    # perimeter is also called as arcLength and we can find directly in python using arcLength function
    approx = cv2.approxPolyDP(i,0.02*perimeter , True)
    #approxPolyDP we have used because it approximates the curve of polygon with the precision
    if(len(approx) == 4):     # 4 means it has 4 corner which will be most probably our number plate as it also has 4 corner
        NumberPlateCount = approx
        #now we will crop that rectanfle part
        x , y , w , h = cv2.boundingRect(i)
        crp_img = image[y:y+h,x:x+w]

                ###############################
                #                             #
        #(y+h)  #                             # let suppose this is our figure with 4 corners
                #                             #
                ###############################
              #(x,y)        ---(x+w)---------->
        #this much part it will crop
        cv2.imwrite(str(name)+ '.png',crp_img)
        name += 1

        break

#now we will draw contour in our main image that we have identified as a number plate
cv2.drawContours(image,[NumberPlateCount],-1,(0,255,0),3)
cv2.imshow("Final Image",image)
cv2.waitKey(0)

# we will crop only the part of number plate
crop_img_loc = '1.png'
cv2.imshow("Cropped Image ",cv2.imread(crop_img_loc))
cv2.waitKey(0)

text = pytesseract.image_to_string(crop_img_loc,lang='eng')
print("Number is : ",text)
cv2.waitKey(0)
