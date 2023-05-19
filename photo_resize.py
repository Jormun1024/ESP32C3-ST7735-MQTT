import os
import cv2

# path = './image'
# filelist = os.listdir(path)
# filelist = sorted(filelist)
i=1
for i in range(1,3):
    f=cv2.imread('./image/'+str(i)+'.jpg')
    img = cv2.resize(f,(128,160),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('./img/img'+str(i)+'.bmp',img)
for i in range(3,8):
    f=cv2.imread('./image/'+str(i)+'.jpg')
    img= cv2.resize(f,(160,128),interpolation=cv2.INTER_CUBIC)
    img_270 = cv2.flip(cv2.transpose(img), 0)
    cv2.imwrite('./img/img'+str(i)+'.bmp',img_270)