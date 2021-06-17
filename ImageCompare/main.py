import cv2
import imutils
from skimage.metrics import structural_similarity as sk_cpt_ssim

image1 = cv2.imread('D:/ImageCompare/img/test1.png')
image2 = cv2.imread('D:/ImageCompare/img/test2.png')

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

(score, diff) = sk_cpt_ssim(gray1, gray2, full = True)
diff = (diff*255).astype("uint8")
print('ssim:{}'.format(score))

thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

for c in cnts:
    [x, y, w, h] = cv2.boundingRect(c)
    cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("Modified", image2)
cv2.imwrite("result.jpg", image2)
cv2.waitKey(0)
