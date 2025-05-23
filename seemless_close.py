import cv2
import numpy as np

dst = cv2.imread("img/objects.png")
cv2.imshow("objects.png", dst)

img = cv2.imread("img/empty.png")
cv2.imshow("fg", img)

mask = np.full_like(img, 255)
 
#--③ 합성 대상 좌표 계산(img2의 중앙)
height, width = dst.shape[:2]
center = (width//2, height//2)
 
#--④ seamlessClone 으로 합성 
normal = cv2.seamlessClone(img, dst, mask, center, cv2.NORMAL_CLONE)
mixed = cv2.seamlessClone(img, dst, mask, center, cv2.MIXED_CLONE)

cv2.imshow('normal', normal)
cv2.imshow('mixed', mixed)

##################################################
# Main Task
##################################################
while True:
    try:
        cv2.getWindowProperty("objects.png", 0)
    except:
        break

    k = cv2.waitKey(0) & 0xFF
    print(f"{k} key pressed")
    if k == 27:
        cv2.destroyAllWindows()
        break
