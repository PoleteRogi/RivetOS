import datetime
from PIL import Image, ImageEnhance, ImageFilter
import sys
import os
import cv2
import numpy
from matplotlib import pyplot as plt
import numpy as np

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
image5 = changeImageSize(1280, 720, image1)
image6 = changeImageSize(1280, 720, image2)
image7 = changeImageSize(1280, 720, image3)
image8 = changeImageSize(1280, 720, image4)

image9 = image5.convert("RGBA")
image10 = image6.convert("RGBA")
image11 = image7.convert("RGBA")
image12 = image8.convert("RGBA")

# Display the image

# alpha-blend the images with varying values of alpha
alphaBlended1 = Image.blend(image9, image10, alpha=.5)

# alphaBlended1 = alphaBlended1.filter(ImageFilter.SHARPEN)

alphaBlended2 = Image.blend(alphaBlended1, image11, alpha=.5)

alphaBlended3 = Image.blend(alphaBlended2, image12, alpha=.5)

enhancer = ImageEnhance.Contrast(alphaBlended3)
alphaBlended3 = enhancer.enhance(1.1)

enhancer = ImageEnhance.Brightness(alphaBlended3)
alphaBlended3 = enhancer.enhance(1)

enhancer = ImageEnhance.Color(alphaBlended3)
alphaBlended3 = enhancer.enhance(1)

now = datetime.datetime.now()

result = cv2.cvtColor(numpy.array(alphaBlended3), cv2.COLOR_RGB2BGR)

#output = cv2.normalize(result, None, 255, 255, cv2.NORM_MINMAX)

output = cv2.detailEnhance(result, sigma_s=.6, sigma_r=0.1)
output = cv2.fastNlMeansDenoisingColored(output, None, 2, 2, 2, 9)

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def gamma_trans(img, gamma):
    gamma_table=[np.power(x/255.0,gamma)*255.0 for x in range(256)]
    gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img,gamma_table)

output = white_balance(output)

cv2.imwrite('./data/fs/camera/' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.png', output)

os.remove('./data/tmp/' + sys.argv[1])
os.remove('./data/tmp/' + sys.argv[2])
os.remove('./data/tmp/' + sys.argv[3])
os.remove('./data/tmp/' + sys.argv[4])