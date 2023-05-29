import datetime
from PIL import Image, ImageEnhance, ImageFilter
import sys
import os
import cv2

# Function to change the image size
def changeImageSize(maxWidth, 
                    maxHeight, 
                    image):
    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage
    
# Take two images for blending them together   
image1 = Image.open('./data/tmp/' + sys.argv[1])
image2 = Image.open('./data/tmp/' + sys.argv[2])
image3 = Image.open('./data/tmp/' + sys.argv[3])
image4 = Image.open('./data/tmp/' + sys.argv[4])

# Make the images of uniform size
image5 = changeImageSize(1280, 800, image1)
image6 = changeImageSize(1280, 800, image2)
image7 = changeImageSize(1280, 800, image3)
image8 = changeImageSize(1280, 800, image4)

image9 = image5.convert("RGBA")

image9 = image9.filter(ImageFilter.SHARPEN)
image9 = image9.filter(ImageFilter.SHARPEN)

image10 = image6.convert("RGBA")
image11 = image7.convert("RGBA")
image12 = image8.convert("RGBA")

# Display the image

# alpha-blend the images with varying values of alpha
alphaBlended1 = Image.blend(image9, image10, alpha=.5)
alphaBlended2 = Image.blend(alphaBlended1, image11, alpha=.25)
alphaBlended3 = Image.blend(alphaBlended2, image12, alpha=.25)

enhancer = ImageEnhance.Contrast(alphaBlended3)
alphaBlended3 = enhancer.enhance(1.075)

enhancer = ImageEnhance.Brightness(alphaBlended3)
alphaBlended3 = enhancer.enhance(1)

enhancer = ImageEnhance.Color(alphaBlended3)
alphaBlended3 = enhancer.enhance(1.15)

now = datetime.datetime.now()

alphaBlended3.save('./data/fs/camera/' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png')

result = cv2.imread('./data/fs/camera/' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png') 
#output = cv2.normalize(result, None, 255, 255, cv2.NORM_MINMAX)
output = cv2.fastNlMeansDenoisingColored(result, None, 4, 4, 4, 6.5)
output = cv2.detailEnhance(output, sigma_s=1.25, sigma_r=0.1)

cv2.imwrite('./data/fs/camera/' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png', output)

os.remove('./data/tmp/' + sys.argv[1])
os.remove('./data/tmp/' + sys.argv[2])
os.remove('./data/tmp/' + sys.argv[3])
os.remove('./data/tmp/' + sys.argv[4])