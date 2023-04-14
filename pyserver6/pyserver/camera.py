import cv2
import time

# VideoCapture オブジェクトを取得します
capture = cv2.VideoCapture(0)

while(True):
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    cv2.imwrite('./static/Image/camera.jpg',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


capture.release()
cv2.destroyAllWindows()