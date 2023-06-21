#!/usr/bin/env python

import numpy as np
from sklearn.cluster import KMeans
from research_dss_app.modules import sysconf
import cv2

def analyzeTeaBuds(project_name,log_file):
    image = cv2.imread(sysconf.getRGBMapPath(project_name,'rgb_map_final.png'))
    sysconf.writeLogRecord("RGB Map path : " + sysconf.getRGBMapPath(project_name,'rgb_map_final.png'),log_file)
    print(sysconf.getRGBMapPath(project_name,'rgb_map_final.png'))
    i_height,i_width,i_channels = image.shape


    # Resize image and make a copy of the original (resized) image.
    if i_width > 0 :
        height = int((i_width / image.shape[1]) * image.shape[0])
        image = cv2.resize(image, (i_width, height),
            interpolation=cv2.INTER_AREA)
    orig = image.copy()

    # Change image color space, if necessary.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    # Flatten the 2D image array into an MxN feature vector, where M is
    # the number of pixels and N is the dimension (number of channels).
    reshaped = image.reshape(image.shape[0] * image.shape[1], image.shape[2])

    # Perform K-means clustering.
    numClusters = max(2,3)
    kmeans = KMeans(n_clusters=numClusters, n_init=40, max_iter=500).fit(reshaped)

    # Reshape result back into a 2D array, where each element represents the
    clustering = np.reshape(np.array(kmeans.labels_, dtype=np.uint8),
        (image.shape[0], image.shape[1]))

    # Sort the cluster labels in order of the frequency with which they occur.
    sortedLabels = sorted([n for n in range(numClusters)],
        key=lambda x: -np.sum(clustering == x))

    # Initialize K-means grayscale image; set pixel colors based on clustering.
    kmeansImage = np.zeros(image.shape[:2], dtype=np.uint8)
    for i, label in enumerate(sortedLabels):
        kmeansImage[clustering == label] = int((255) / (numClusters - 1)) * i

    # Concatenate original image and K-means image, separated by a gray strip.
    concatImage = np.concatenate((orig,
        193 * np.ones((orig.shape[0], int(0.0625 * orig.shape[1]), 3), dtype=np.uint8),
        cv2.cvtColor(kmeansImage, cv2.COLOR_GRAY2BGR)), axis=1)
    #cv2.imshow('Original vs clustered', concatImage)

    sysconf.writeLogRecord('Clustered RGB map path : ' + sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed.png'),log_file)
    cv2.imwrite(sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed_before.png'),kmeansImage)

    image = cv2.imread(sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed_before.png'),1)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)

    width = image.shape[1]
    height = image.shape[0]

    for i in range(height):
        for j in range(width):
            if((image[i][j][0] != 127) & (image[i][j][1] != 127) & (image[i][j][2] != 127)):
                image[i][j] = (0,0,0,0)

    cv2.imwrite(sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed.png'),image)
    # return rgb_map.split('.')[0] + '_processed.jpg'
