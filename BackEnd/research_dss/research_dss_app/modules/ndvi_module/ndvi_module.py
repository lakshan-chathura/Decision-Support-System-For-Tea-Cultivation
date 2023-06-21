#!/usr/bin/env python

# from plantcv import plantcv as pcv
import cv2
import numpy as np
import argparse
# import PIL as Image
from research_dss_app.modules import sysconf
from datetime import datetime
def createNDVIMap(nir_path,rgb_path,ndvi_path,log_file):
    # Set debug mode to plot
    # pcv.params.debug = "plot"

    print("RGB Map Path : " + rgb_path)
    print("NIR Map Path : " + nir_path)
    # Read the RGB image
    #rgb, _, _ = pcv.readimage(rgb_path, mode="RGB")
    rgb = cv2.imread(rgb_path,1)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2BGRA)
    print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Converting the NIR and RGB maps to RGBA mode',end="")
    sysconf.writeLogRecord('Reading and converting RGB map to RGBA',log_file)
    sysconf.writeLogRecord('RGB image resolution is ' + str(rgb.shape[0]) + ' x ' + str(rgb.shape[1]),log_file)
    # rgb, _, _ = pcv.readimage(nir_path, mode="GRAY")
    # Read the NIR image
    # nir, _, _ = pcv.readimage(nir_path, mode="GRAY")
    # nir, _, _ = pcv.readimage(nir_path, mode="RGB")
    nir = cv2.imread(nir_path,1)
    nir = cv2.cvtColor(nir,cv2.COLOR_BGR2BGRA)
    sysconf.writeLogRecord('Reading and converting non pure NIR map to RGBA',log_file)
    sysconf.writeLogRecord('NIR image resolution is ' + str(nir.shape[0]) + ' x ' + str(nir.shape[1]),log_file)
    # print("nir : " + str(nir.shape))
    # print("rgb : " + str(rgb.shape))
    print('.....done')
    width = rgb.shape[1]
    height = rgb.shape[0]
    flag = ''

    print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "Resizing the NIR and RGB map arrays",end="")
    sysconf.writeLogRecord('Resizing RGB and NIR map numpy arrays started',log_file)
    if(nir.shape[0] < rgb.shape[0]):
        # print('rgb height : ' + str(rgb.shape[0]))
        # print('nir height : ' + str(nir.shape[0]))
        height = nir.shape[0]
        flag = 'nir'
    else:
        # print('nir height : ' + str(nir.shape[0]))
        # print('rgb height : ' + str(rgb.shape[0]))
        height = rgb.shape[0]
        flag = 'rgb'

    if(nir.shape[1] < rgb.shape[1]):
        # print('rgb height : ' + str(rgb.shape[1]))
        # print('nir height : ' + str(nir.shape[1]))
        width = nir.shape[1]
        flag = 'nir'
    else:
        # print('nir height : ' + str(nir.shape[1]))
        # print('rgb height : ' + str(rgb.shape[1]))
        width = rgb.shape[1]
        flag = 'rgb'

    sysconf.writeLogRecord('New RGB and NIR image resolution is ' + str(height) + ' x ' + str(width),log_file)
    # sysconf.writeLogRecord('New NIR image resolution is ' + nir.shape[0] + ' x ' + nir.shape[1])
    # if(flag == 'rgb'):
    nir = cv2.resize(nir,(width,height))
    rgb = cv2.resize(rgb,(width,height))
    print('.....done')
    print('New RGB and NIR image resolution is ' + str(height) + ' x ' + str(width))
    sysconf.writeLogRecord('Resizing RGB and NIR map numpy arrays completed',log_file)

    # Calculate NDVI
    ndvi = np.zeros((height,width,1),dtype=np.float64)

    print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "Constructing NDVI map layers",end="")
    sysconf.writeLogRecord('Constructing NDVI and NDVI map layer arrays..0 of 3 completed',log_file)
    ndvi_pixel_np_red_layer_array = np.zeros((height,width,4),dtype=np.uint8)
    sysconf.writeLogRecord('Constructing NDVI and NDVI map layer arrays 1 of 3 completed',log_file)
    ndvi_pixel_np_green_layer_array = np.zeros((height,width,4),dtype=np.uint8)
    sysconf.writeLogRecord('Constructing NDVI and NDVI map layer arrays..2 of 3 completed',log_file)
    ndvi_pixel_np_blue_layer_array = np.zeros((height,width,4),dtype=np.uint8)
    sysconf.writeLogRecord('Constructing NDVI and NDVI map layer arrays..3 of 3 completed',log_file)

    for i in range(height):
        for j in range(width):
            ndvi[i][j] = (math.floor(((nirIntensity - float(rgb[i][j][2]))/(nirIntensity + float(rgb[i][j][2]))) * 100))/100
            value = ndvi_map[i][j]

            if((value <= 1.00) & (value >= 0.20)):
                ndvi_pixel_np_green_layer_array[i][j] = (0,255,0,255)
                ndvi_pixel_np_red_layer_array[i][j] = (0,255,0,0)
                ndvi_pixel_np_blue_layer_array[i][j] = (0,255,0,0)
            elif((value > 0) & (value < 0.20)):
                ndvi_pixel_np_green_layer_array[i][j] = (0,0,255,0)
                ndvi_pixel_np_red_layer_array[i][j] = (0,0,255,255)
                ndvi_pixel_np_blue_layer_array[i][j] = (0,0,255,0)
            elif((value <= 0) & (value >= -0.5)):
                ndvi_pixel_np_green_layer_array[i][j] = (0,255,0,255)
                ndvi_pixel_np_red_layer_array[i][j] = (0,255,0,0)
                ndvi_pixel_np_blue_layer_array[i][j] = (0,255,0,0)
            elif((value <= -0.5) & (value >= -0.7)):
                ndvi_pixel_np_green_layer_array[i][j] = (255,0,0,0)
                ndvi_pixel_np_red_layer_array[i][j] = (255,0,0,0)
                ndvi_pixel_np_blue_layer_array[i][j] = (255,0,0,255)
            elif((value <= -0.7) & (value >= -1.00)):
                ndvi_pixel_np_green_layer_array[i][j] = (0,0,255,0)
                ndvi_pixel_np_red_layer_array[i][j] = (0,0,255,255)
                ndvi_pixel_np_blue_layer_array[i][j] = (0,0,255,0)

    # Make a pseudocolored NDVI image
    # ndvi_pseudo = pcv.visualize.pseudocolor(gray_img=ndvi, min_value=-1, max_value=1, cmap="viridis")

    # cv2.imwrite(ndvi_path + '.png',ndvi_pixel_np_array)
    print('.....done')
    print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Writing NDVI map layers',end="")
    sysconf.writeLogRecord('Writing NDVI map layers',log_file)
    cv2.imwrite(ndvi_path  + '_red_layer.png',ndvi_pixel_np_red_layer_array)
    cv2.imwrite(ndvi_path  + '_green_layer.png',ndvi_pixel_np_green_layer_array)
    cv2.imwrite(ndvi_path  + '_blue_layer.png',ndvi_pixel_np_blue_layer_array)
    print('.....done')
    # return ndvi_path,ndvi
    return ndvi

def calculateHealthyAndNonHealthyPlantPercentage(ndvi_map):#(ndvi_path,ndvi_map):
    # ndvi_map, _, _ = pcv.readimage(ndvi_path, mode="RGB")
    # ndvi_map = ndvi_map.astype(np.float64)
    width = ndvi_map.shape[1]
    height = ndvi_map.shape[0]
    healthy_pixel_total = 0
    unhealthy_pixel_total = 0
    non_plant_pixel_total = 0
    print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Analyzing the NDVI array',end="")
    for i in range(height):
        for j in range(width):
            value = ndvi_map[i][j]
            ndvi[i][j] = (math.floor(((nirIntensity - float(rgb[i][j][2]))/(nirIntensity + float(rgb[i][j][2]))) * 100))/100
            value = ndvi_map[i][j]

            if((value <= 1.00) & (value >= 0.20)):
                healthy_pixel_total = healthy_pixel_total + 1
            elif((value > 0) & (value < 0.20)):
                unhealthy_pixel_total = unhealthy_pixel_total + 1
            elif((value <= 0) & (value >= -0.5)):
                healthy_pixel_total = healthy_pixel_total + 1
            elif((value <= -0.5) & (value >= -0.7)):
                non_plant_pixel_total = non_plant_pixel_total + 1
            elif((value <= -0.7) & (value >= -1.00)):
                unhealthy_pixel_total = unhealthy_pixel_total + 1

    print('.....done')
    return {
            "Good_health":round((healthy_pixel_total/(height*width))*100,2),
            "Bad_health":round((unhealthy_pixel_total/(height*width))*100,2),
            "Non_plants":round((non_plant_pixel_total/(height*width))*100,2)
            }
