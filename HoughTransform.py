import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def linesdetection(imgNum):
    img = cv.imread("image"+imgNum+".png",0)
    
    #img = cv.equalizeHist(img)
    
    img = cv.Canny(img, 200, 180) 
    
    img = cv.bitwise_not(img)
    
    diag = int((np.sqrt(pow(len(img),2)+pow(len(img[0]),2)))+1)
    
    matrix = np.zeros((diag*2,180))
    matrix2 = np.zeros((diag*2,180))
    
    for x in range(0,len(img)):
        for y in range(0,len(img[x])):
            if img[x][y] == 0:
                for theta in range(0,180):
                    p = int(x*np.sin(np.deg2rad(theta)) + y*np.cos(np.deg2rad(theta)))
                    matrix[p+diag,theta] += 1
    
    lines = []
    
    for x in range(0,len(img)):
        for y in range(0,len(img[x])):
            if img[x][y] == 0:
                auxx = 0
                auxy = 0
                maxx = -100
                for theta in range(0,180):
                    p = int(np.round(x*np.sin(np.deg2rad(theta)) + y*np.cos(np.deg2rad(theta))))
                    if matrix[p+diag,theta] >= maxx:
                        auxx = p+diag
                        auxy = theta
                        maxx = matrix[auxx,auxy]
                if maxx >= 0:
                    matrix2[auxx,auxy] += 1
    
    for x in range(0,len(matrix2)):
        for y in range(0,len(matrix2[x])):
            if matrix2[x][y] != 0:
                lines.append([x,y])
    
    linesstraight = []
    
    for line in lines:
        theta = np.deg2rad(line[1])
        c = np.cos(theta)
        s = np.sin(theta)
        point = (int((line[0]-diag)*c), int((line[0]-diag)*s)) 
        vec = (-s,c)
        if abs(c) >= abs(s):
            displacement = -(point[1]/vec[1])
        else:
            displacement = -(point[0]/vec[0])
        point = (int(point[0] + displacement*vec[0]),int(point[1] + displacement*vec[1]))
        change = True
        while change:
            change = False
            if point[0] > (len(img[0]) - 1):
                displacement = (len(img[0]) - 1 - point[0])/vec[0]
                change = True
            if point[1] > (len(img) - 1):
                displacement = (len(img) - 1 - point[1])/vec[1]
                change = True
            if point[0] < 0:
                displacement = -(point[0]/vec[0])
                change = True
            if point[1] < 0:
                displacement = -(point[1]/vec[1])
                change = True
            if change:
                point = (int(point[0] + displacement*vec[0]),int(point[1] + displacement*vec[1])) 
        if (point[0] == 0 and vec[0] < 0) or (point[0] == (len(img[0]) - 1) and vec[0] >0):
            vec = (-vec[0],-vec[1])
        if (point[1] == 0 and vec[1] < 0) or (point[1] == (len(img) - 1) and vec[1] >0):
            vec = (-vec[0],-vec[1])
			
        sequenceblack = 10
        sequence = 0
        matriks = [(0,0),(0,0),0]
        while int(np.round(point[0])) < len(img[0]) and int(np.round(point[1])) < len(img) and int(np.round(point[0])) >= 0 and int(np.round(point[1])) >= 0:
           black = False
           for auxx in range(-1,2):
               for auxy in range(-1,2):
                   try:
                       if img[int(np.round(point[1]))+auxx][int(np.round(point[0]))+auxy] == 0:
                           black = True
                       if black: break
                   except: {}
           if black:
               if sequence == 0:
                   matriks[0] = (int(np.round(point[0])),int(np.round(point[1])))
               sequence += 1
           else:
               if sequence >= sequenceblack:
                   matriks[1] = (int(np.round(point[0])),int(np.round(point[1])))
                   matriks[2] = sequence
                   linesstraight.append(matriks)
                   matriks = [(0,0),(0,0),0]
               sequence = 0
           point = (point[0] + vec[0], point[1] + vec[1])
        if sequence >= sequenceblack:
           matriks[1] = (int(np.round(point[0])),int(np.round(point[1])))
           matriks[2] = sequence
           linesstraight.append(matriks)
           matriks = [(0,0),(0,0),0]
           sequence = 0
    
    img = np.zeros([len(img),len(img[0]),1])
    img.fill(255)
    
    idx = -1
    for i in range(3):
        cv.line(img,linesstraight[idx][0],linesstraight[idx][1],(0,0,0),1)
        idx -= 1

   # apabila ingin di print semua linenya, bukan hanya 3
    #for linestraight in linesstraight:
     #   cv.line(img,linestraight[0],linestraight[1],(0,0,0),1)
	
  # plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.savefig(str("Hough"+imgNum+".jpg"))
    cv.imwrite(str("NewImage"+imgNum+".png"),img)
    with open("linesImage"+imgNum+".txt", mode='w') as file:
        for i in range(3): 
		# for i i in range(0,len(linesstraight)): // print semua line
            file.write("Line "+ str(i) + ": " + str(linesstraight[i][0]) + " to " + str(linesstraight[i][1])+"\n")

if __name__ == '__main__':
	linesdetection("1")
	linesdetection("2")
	linesdetection("3")
	linesdetection("4")
	linesdetection("5")
	linesdetection("6")


