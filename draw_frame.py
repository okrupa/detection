import numpy as np
import cv2

img = cv2.imread('frame0000.jpg', cv2.IMREAD_COLOR)

cv2.rectangle(img, (500,250), (1000,500), (0,0,255), 2)
pts = np.array([[100,50], [200,300], [700,200], [500,100]], np.int32)
#pts = pts.reshape((-1, 1, 2))
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()





# draw line
#cv2.line(img, (0, 0), (50,100), (0,0,0), 1)
#                    y,  x (dolny wierzcholek po lewej stronie)       
#cv2.rectangle(img, (500,250), (1000,500), (0,0,255), 2)            # (0, 0, 255) - kolor ramki, 2 - szerokość
#                                 y,  x (górny wierzchołek po prawej stronie)