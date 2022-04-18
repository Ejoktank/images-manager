#!/usr/bin/env python

import cv2
import os
import pandas as pd
from PIL import Image
from PIL import ImageStat
from PIL import ImageEnhance
import numpy as np
from sklearn.preprocessing import normalize
from sklearn import preprocessing


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def calculate_brightness(file):
    im = Image.open(file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def calculate_contrast(image):
    return np.sqrt(((image - image.mean(axis=0))**2).mean())


def calculate_sharpness(img):
    edges = cv2.Canny(img, 100, 300)
    non_zero_count = np.count_nonzero(edges)
    height, width = img.shape[:2]
    return non_zero_count * 1000.0 / (height * width)


row = 0
df = pd.DataFrame(columns=['Filename', 'VarOfLaplacian', 'Brightness', 'Contrast', 'Sharpness'])

for file in os.listdir(os.getcwd()):
    if (file.endswith(".tif") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")):
        image = cv2.imread(file, 0)


focus_measure = variance_of_laplacian(image)
brightness = calculate_brightness(file)
contrast = calculate_contrast(image)
sharpness = calculate_sharpness(image)
df.loc[row] = [file, focus_measure, brightness, contrast, sharpness]
row += 1

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')

x = df.loc[:, 'VarOfLaplacian':'Sharpness']
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_norm = pd.DataFrame(x_scaled)

df.to_excel(writer, 'Sheet1')
df_norm.to_excel(writer, 'Sheet2')

writer.save()
