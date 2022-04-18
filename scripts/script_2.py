# -*- coding: utf-8 -*-

import numpy as np 
import cv2
import os
import math

cwd = os.getcwd()
outputFolder = cwd + "/Output/"
closedFolder = cwd + "/Closed/"
edgedFolder = cwd + "/Edged/"
inputFilesCount = len(next(os.walk(cwd))[2]) - 1  # -1 - сам файл программы


def get_file_name(n): 
    if n > 99:
        num = str(n) 
    elif n > 9:
        num = '0' + str(n) 
    else:
        num = '00' + str(n)
    return 'video1 ' + num + '.jpg'


def find_angle(edge1, edge2):
    a = edge1[0]*edge2[0] + edge1[1]*edge2[1] 
    b = cv2.norm(edge1) * cv2.norm(edge2) 
    div = a / b
    if abs(div) > 1:
        div = 1
    return 180.0/math.pi * math.acos(div)


def check_angle(angle):
    return angle is not None and angle < 126 and angle > 64


def check_angles(box):
    edge1 = np.int0((box[1][0][0] - box[0][0][0], box[1][0][1] - box[0][0][1])) 
    edge2 = np.int0((box[2][0][0] - box[1][0][0], box[2][0][1] - box[1][0][1])) 
    edge3 = np.int0((box[3][0][0] - box[2][0][0], box[3][0][1] - box[2][0][1])) 
    edge4 = np.int0((box[0][0][0] - box[3][0][0], box[0][0][1] - box[3][0][1]))

    angle1 = find_angle(edge1, edge2) 

    if not check_angle(angle1):
        return False
    angle2 = find_angle(edge2, edge3) 

    if not check_angle(angle2):
        return False
    angle3 = find_angle(edge3, edge4) 

    if not check_angle(angle3):     
        return False
    angle4 = find_angle(edge4, edge1) 

    if not check_angle(angle4):
        return False 
    
    return True


def find_circut(n):
    # загружаем изображение, меняем цвет на оттенки серого и уменьшаем резкость
    # имя файла, который будем анализировать 
    image = cv2.imread(fn)
    
    fn = get_file_name(n)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.GaussianBlur(gray, (29, 29), 2)
    unsharp_image = cv2.addWeighted(blured, 1, blured, 1.3, 0, blured)
    # распознавание контуров

    # применяем закрытие
    edged = cv2.Canny(unsharp_image, 10, 300) 
    cv2.imwrite(os.path.join(edgedFolder, "edged" + str(n) + ".jpg"), edged)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))

    # найдем контуры в изображенииe
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel) 
    cv2.imwrite(os.path.join(closedFolder, "closed" + str(n) + ".jpg"), closed)
    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1] 
    total = 0

    # цикл по контурам 
    for c in cnts:
        rect = cv2.minAreaRect(c)
    # вычисляем периметр 
    
    # аппрокс. контур, чтобы избежать влияния шумов 
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        peri = cv2.arcLength(c, True)
        if len(approx) != 4:
            continue

    # ищем площадь прямоугольника 
        area = int(rect[1][0] * rect[1][1])
        if area < 3000:
            continue

    # проверяем углы прямоугольника на соответствие пороговым значениям

        isRect = check_angles(approx) 
        if not isRect:
            continue

    cv2.drawContours(image, [approx], -1, (0, 255, 0), 4) 
    total += 1

    # показываем результирующее изображение if total != 0:

    print("Я нашёл {0} объект(а) на ".format(total) + "example" + str(n) + ".jpg")

    cv2.imwrite(os.path.join(outputFolder, "output" + str(n) + ".jpg"), image)

    for n in range(1, inputFilesCount):
        find_circut(n)
