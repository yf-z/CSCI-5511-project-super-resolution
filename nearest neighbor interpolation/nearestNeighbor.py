import numpy as np
from scipy.interpolate import RegularGridInterpolator
import cv2
from PIL import Image


def neareastNeighbor(fileName, n):
    inputImage = cv2.imread(fileName)

    rowNum = inputImage.shape[0]
    colNum = inputImage.shape[1]

    red = inputImage[:,:,2]
    green = inputImage[:,:,1]
    blue = inputImage[:,:,0]

    newRed = newArray(red, rowNum, colNum, n)
    newgreen = newArray(green, rowNum, colNum, n)
    newblue = newArray(blue, rowNum, colNum, n)

    newData = np.zeros([rowNum*n-n, colNum*n-n, 3], dtype=np.uint8)
    for i in range(rowNum*n-n):
        for j in range(colNum*n-n):
            newData[i,j] = [newRed[i,j], newgreen[i,j], newblue[i,j]]

    print(newData.shape)
    
    img = Image.fromarray(newData, 'RGB')
    img.save('valid_1_noblur@4times.png')
    img.show()

def f(x,y,array,n):
    newx = int((x-1)/n)
    newy = int((y-1)/n)
    return array[newx, newy]

def newArray(array, rowNum, colNum, n):
    x = np.arange(1, rowNum*n, n)
    y = np.arange(1, colNum*n, n)

    data = array

    my_interpolating_function = RegularGridInterpolator((x, y), data)

    newArr = np.zeros([rowNum*n-n, colNum*n-n])
    for i in range(rowNum*n-n):
        for j in range(colNum*n-n):
            if (i+1 not in x) or (j+1 not in y):
                print(i+1,j+1)
                newArr[i,j] = my_interpolating_function(np.array([[i+1,j+1]]))
            else:
                newArr[i,j] = f(i,j,array,n)
    
    return newArr

if __name__ == "__main__":
    neareastNeighbor("valid_lr_1noblur.png", 4)