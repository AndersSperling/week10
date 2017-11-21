import numpy as np
import cv2

#Loading PeerGrade logo and resize it to 10x10
img1 = cv2.imread('pgLogo.jpg',0)
reI1 = cv2.resize(img1, (10, 10))

#Loading PeerGrade logo
img1C1 = cv2.imread('pgLogo.jpg',0)

#Change pixel 100 to 150 in x and y direction to value 246
for num in range(100,200):
    for i in range(100,200):
        img1C1[num,i] = 246
        
#Resize the changed image to 10x10
reI1C1 = cv2.resize(img1C1, (10, 10))

#Loading PeerGrade logo
img1C2 = cv2.imread('pgLogo.jpg',0)

#Change pixel 100 to 150 in x and y direction to value 230
for num in range(100,150):
    for i in range(100,150):
        img1C2[num,i] = 230
        
#Resize the changed image to 10x10
reI1C2 = cv2.resize(img1C2, (10, 10))

#Loading PeerGrade cover image and resize it to 10x10
img2 = cv2.imread('pg.png',0)
reI2 = cv2.resize(img2,(10,10))

#Compare adjacent values
re1C1 = reI1C1<reI1
re1C2 = reI1C2<reI1
re1C3 = reI2<reI1

#Convert to hash and print
print(hash(str(re1C1)))
print(hash(str(re1C2)))
print(hash(str(re1C3)))