#!/usr/bin/env python

import os
import time
import pathlib
from PIL import Image
import cv2
import numpy as np
from research_dss_app.modules import sysconf
# from research_dss_app.modules.mapping_module import odm_module
from subprocess import call
import shutil

def writeImageNamesToTextFile(file_name):
	bands = list()
	with open (file_name) as fin:
    		for line in fin:
        		bands.append(line.strip())
	return bands

def sortTheImagesInTextFiles(band,file_name):
	band.sort()
	# print(band)
	with open(file_name,'w') as fout:
    		for image_name in band:
        		fout.write(image_name+'')
	return band

def geotagImage(source_folder,source_file_name,target_folder,targer_file_name,coordinate,log_file):
	gps_coordinate = ""
	command = ""
	if(coordinate == "latitude"):
		command = "exiftool -tagsfromfile " + source_folder + "/" + source_file_name + " -GPSLatitude " + target_folder + "/" + targer_file_name
	elif(coordinate == "longtitude"):
		command = "exiftool -tagsfromfile " + source_folder + "/" + source_file_name + " -GPSLongitude " + target_folder + "/" + targer_file_name
	# print(command)
	os.system(command)
	sysconf.writeLogRecord('Geotagging coordinate type : ' + coordinate,log_file)
	sysconf.writeLogRecord('Geotagging coordinate command : ' + command,log_file)
	# try:
	# 	shutil.rmtree('rm -r ' + target_folder + "/" + targer_file_name + "_original")
	# except OSError as e:
	# 	print ("Error: %s - %s." % (e.filename, e.strerror))
	# os.system('rm -r ' + target_folder + "/" + targer_file_name + "_original")

def geotagging_images(project_name,log_file):
	RGB_PATH = sysconf.getRGBRawImagesPath(project_name)
	NIR_PATH = sysconf.getNIRRawImagesPath(project_name)
	RGB_IMG_GEODATA_LOG_PATH = sysconf.getRGBGeoDataLogPath(project_name,'rgb_img_log.txt')
	NIR_IMG_GEODATA_LOG_PATH = sysconf.getNIRGeoDataLogPath(project_name,'nir_img_log.txt')

	sysconf.writeLogRecord('RGB images path : '  + RGB_PATH,log_file)
	sysconf.writeLogRecord('RGB images geo data log path : '  + RGB_IMG_GEODATA_LOG_PATH,log_file)
	sysconf.writeLogRecord('NIR images path : '  + NIR_PATH,log_file)
	sysconf.writeLogRecord('NIR images geo data log path : '  + NIR_IMG_GEODATA_LOG_PATH,log_file)

	# os.system("exiftool -p '$filename' -q -f " + NIR_PATH + ">" + NIR_IMG_GEODATA_LOG_PATH)
	# os.system("exiftool -p '$filename' -q -f " + RGB_PATH + ">" + RGB_IMG_GEODATA_LOG_PATH)

	sysconf.writeLogRecord('exif command for RGB images : ' + "exiftool -p '$filename' -q -f " + RGB_PATH + ">" + RGB_IMG_GEODATA_LOG_PATH,log_file)
	sysconf.writeLogRecord('exif command for NIR images : ' + "exiftool -p '$filename' -q -f " + NIR_PATH + ">" + NIR_IMG_GEODATA_LOG_PATH,log_file)

	###sort RGB_names.txt file
	rgb_band = writeImageNamesToTextFile(RGB_IMG_GEODATA_LOG_PATH)
	rgb_band = sortTheImagesInTextFiles(rgb_band,RGB_IMG_GEODATA_LOG_PATH)

	 ####sort NIR_names.txt file
	nir_band = writeImageNamesToTextFile(NIR_IMG_GEODATA_LOG_PATH)
	nir_band = sortTheImagesInTextFiles(nir_band,NIR_IMG_GEODATA_LOG_PATH)

	###geotagging
	for x in range(len(rgb_band)):
		geotagImage(RGB_PATH,rgb_band[x],NIR_PATH,nir_band[x],"latitude",log_file)
		geotagImage(RGB_PATH,rgb_band[x],NIR_PATH,nir_band[x],"longtitude",log_file)

def Create_Orthomap(project_name,mode,log_file):
	ODM_EXEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'ODMStarter.sh')
	sysconf.writeLogRecord('ODM execution shell script path : ' + ODM_EXEC_PATH,log_file)
	PROJECT_PATH = ''#sysconf.getRGBRawImagesPath(project_name)
	mapPath = ''
	if((mode == 'NIR') or (mode == 'nir')):
		PROJECT_PATH = (sysconf.getNIRRawImagesPath(project_name)).split('/' + project_name)
		mapPath = sysconf.getNIRRawMapPath(project_name)
	elif((mode == 'RGB') or (mode == 'rgb')):
		PROJECT_PATH = (sysconf.getRGBRawImagesPath(project_name)).split('/' + project_name)
		mapPath = sysconf.getRGBRawMapPath(project_name)

	sysconf.writeLogRecord('Project path : ' + str(PROJECT_PATH),log_file)
	sysconf.writeLogRecord('Map path : ' + mapPath,log_file)
	sysconf.writeLogRecord('ODM execution command : ' + 'gnome-terminal -x ' + ODM_EXEC_PATH + ' ' + project_name + ' ' + PROJECT_PATH[0] + ' ' + sysconf.getODMExecutablePath(),log_file)

	# print('PROJECT_PATH : ' + str(PROJECT_PATH))
	# print('mapPath : ' + mapPath)

	os.system('gnome-terminal -x ' + ODM_EXEC_PATH + ' ' + project_name + ' ' + PROJECT_PATH[0] + ' ' + sysconf.getODMExecutablePath())

	if(pathlib.Path(mapPath).exists() == False):
		while(pathlib.Path(mapPath).exists() == False):
			time.sleep(1)

def Image_Overlap(latter_image,upper_image,map_destination_path,log_file):
	MIN_MATCH_COUNT = 4

	## prepare data
	img1 = cv2.imread(latter_image)
	img2 = cv2.imread(upper_image)

	gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


	## Create SIFT object
	sift = cv2.xfeatures2d.SIFT_create()

	## Create flann matcher
	matcher = cv2.FlannBasedMatcher(dict(algorithm = 1, trees = 5), {})

	## Detect keypoints and compute keypointer descriptors
	kpts1, descs1 = sift.detectAndCompute(gray1,None)
	kpts2, descs2 = sift.detectAndCompute(gray2,None)

	## knnMatch to get Top2
	matches = matcher.knnMatch(descs1, descs2, 2)
	# Sort by their distance.
	matches = sorted(matches, key = lambda x:x[0].distance)

	## Ratio test, to get good matches.
	good = [m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]

	canvas = img2.copy()

	## find homography matrix
	if len(good)>MIN_MATCH_COUNT:

    		## (queryIndex for the small object, trainIndex for the scene )
    		src_pts = np.float32([ kpts1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    		dst_pts = np.float32([ kpts2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

			## find homography matrix in cv2.RANSAC using good match points
    		M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

    		h,w = img1.shape[:2]
    		pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    		dst = cv2.perspectiveTransform(pts,M)

    		cv2.polylines(canvas,[np.int32(dst)],True,(0,255,0),3, cv2.LINE_AA)
	else:
    		print( "Not enough matches are found - {}/{}".format(len(good),MIN_MATCH_COUNT))


	## drawMatches
	matched = cv2.drawMatches(img1,kpts1,canvas,kpts2,good,None)#,**draw_params)

	## Crop the matched region from Orthomap
	h,w = img1.shape[:2]
	pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
	dst = cv2.perspectiveTransform(pts,M)
	perspectiveM = cv2.getPerspectiveTransform(np.float32(dst),pts)
	found = cv2.warpPerspective(img2,perspectiveM,(w,h))

	## save and display
	cv2.imwrite("matched.png", matched)
	cv2.imwrite(map_destination_path, found)
	sysconf.writeLogRecord('Pre processed map image destination path : ' + map_destination_path,log_file)
	#Remove the black area
	resultant_file_name = map_destination_path.split('/').pop()
	img = cv2.imread(map_destination_path)

	grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, thresholded = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY)
	bbox = cv2.boundingRect(thresholded)
	x, y, w, h = bbox
	foreground = img[y:y+h, x:x+w]
	finalPath = map_destination_path.split('/')[:-1]
	finalPath = '/'.join(finalPath)
	cv2.imwrite(os.path.join(finalPath,resultant_file_name.split('.')[0] + '_final.png'),foreground)
	sysconf.writeLogRecord('Final produced map image : ' + os.path.join(finalPath,resultant_file_name.split('.')[0] + '_final.png'),log_file)
	return resultant_file_name.split('.')[0] + '_final.png'
	# os.system('rm -r ' + finalPath + '/' + resultant_file_name)

def createGeoTiff(project_name,mode,log_file):
	rawMapPath = ''
	resultantMapName = []
	if (mode == 'rgb'):
		rawMapPath = sysconf.getRGBRawMapPath(project_name)
		resultantMapName =[sysconf.getRGBMapPath(project_name,'rgb_map_final.png')]
	elif (mode == 'nir'):
		rawMapPath = sysconf.getNIRRawMapPath(project_name)
		resultantMapName = [sysconf.getNIRMapPath(project_name,'nir_map_final.png')]
	elif (mode == 'ndvi'):
		rawMapPath = sysconf.getRGBMapPath(project_name,'rgb_map_final.tif')
		resultantMapName = [sysconf.getNDVIMapPath(project_name,'ndvi_map_final_red_layer.png'),sysconf.getNDVIMapPath(project_name,'ndvi_map_final_green_layer.png'),sysconf.getNDVIMapPath(project_name,'ndvi_map_final_blue_layer.png')]
	elif (mode == 'cluster'):
		rawMapPath = sysconf.getRGBMapPath(project_name,'rgb_map_final.tif')
		resultantMapName = [sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed.png')]

	for index in range(len(resultantMapName)):
		# print()
		# print('gdalinfo ' + rawMapPath + ' > ' + resultantMapName[index] + '_gdaldata.txt')
		# print(resultantMapName[index] + '_gdaldata.txt')
		# print()
		sysconf.writeLogRecord('Source map is ' + rawMapPath,log_file)
		sysconf.writeLogRecord('Resultant map is ' + resultantMapName[index],log_file)
		sysconf.writeLogRecord('Geo data retrieval command : gdalinfo ' + rawMapPath + ' > ' + resultantMapName[index] + '_gdaldata.txt',log_file)
		os.system('gdalinfo ' + rawMapPath + ' > ' + resultantMapName[index] + '_gdaldata.txt')
		content = open(resultantMapName[index] + '_gdaldata.txt','r').read()
		content = content.split('Corner Coordinates:')[1].split('Band 1')

		content = content[0].split('\n')
		upperLeft = content[1].split('(')[1].split(')')[0].split('  ')[1].split(',')
		lowerRight = content[4].split('(')[1].split(')')[0].split('  ')[1].split(',')

		upperLeftX = upperLeft[0]
		upperLeftY = upperLeft[1].split(' ')[1]
		lowerRightX = lowerRight[0]
		lowerRightY = lowerRight[1].split(' ')[1]
		# print(upperLeftX)
		# print(upperLeftY)
		# print(lowerRightX)
		# print(lowerRightY)

		sysconf.writeLogRecord('GDAL translation command : gdal_translate -a_ullr ' + upperLeftX + ' ' + upperLeftY + ' ' + lowerRightX + ' '+ lowerRightY +' -co TILED=yes  -co BIGTIFF=IF_SAFER -co COMPRESS=DEFLATE -co PREDICTOR=2  -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -co NUM_THREADS=8 -a_srs "+units=m +no_defs=True +datum=WGS84 +proj=utm +zone=17 " --config GDAL_CACHEMAX 31.6% ' + resultantMapName[index] + ' '+ resultantMapName[index].split('.')[0] +'.tif',log_file)
		if (mode == 'ndvi'):
			sysconf.writeLogRecord('##################################################################',log_file)
		os.system('gdal_translate -a_ullr ' + upperLeftX + ' ' + upperLeftY + ' ' + lowerRightX + ' '+ lowerRightY +' -co TILED=yes  -co BIGTIFF=IF_SAFER -co COMPRESS=DEFLATE -co PREDICTOR=2  -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 -co NUM_THREADS=8 -a_srs "+units=m +no_defs=True +datum=WGS84 +proj=utm +zone=17 " --config GDAL_CACHEMAX 31.6% ' + resultantMapName[index] + ' '+ resultantMapName[index].split('.')[0] +'.tif')

def createTiles(project_name,mode,log_file):
	map_path = []
	destination_map_path = []
	map_name = []
	tile_path = []
	if mode == 'rgb':
		destination_map_path = [sysconf.getRGBMapPath(project_name,'rgb_map_final.tif')]
		map_path = [sysconf.getRGBRawMapPath(project_name)]
		map_name = ['rgb_map_final']
	elif mode == 'nir':
		destination_map_path = [sysconf.getNIRMapPath(project_name,'nir_map_final.tif')]
		map_path = [sysconf.getNIRRawMapPath(project_name)]
		map_name = ['nir_map_final']
	elif mode == 'ndvi':
		destination_map_path = [sysconf.getNDVIMapPath(project_name,'ndvi_map_final_red_layer.tif'),sysconf.getNDVIMapPath(project_name,'ndvi_map_final_green_layer.tif'),sysconf.getNDVIMapPath(project_name,'ndvi_map_final_blue_layer.tif')]
		map_path = [sysconf.getNDVIMapPath(project_name,'ndvi_map_final_red_layer.tif'),sysconf.getNDVIMapPath(project_name,'ndvi_map_final_green_layer.tif'),sysconf.getNDVIMapPath(project_name,'ndvi_map_final_blue_layer.tif')]
		map_name = ['ndvi_map_final_red_layer','ndvi_map_final_green_layer','ndvi_map_final_blue_layer']
	elif mode == 'cluster':
		destination_map_path = [sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed.tif')]
		map_path = [sysconf.getTeaBudIndetifiedMapPath(project_name,'rgb_processed.tif')]
		map_name = ['rgb_processed']
	for index in range(len(destination_map_path)):
		sysconf.writeLogRecord('Map path : ' + map_path[index],log_file)
		sysconf.writeLogRecord('Tile path : ' + destination_map_path[index],log_file)

		# os.system('cp ' + map_path + ' ' + destination_map_path)
		sysconf.writeLogRecord('gdal2tiles log file in ' + sysconf.createLogFile(project_name + '_' + mode + '_tiling.txt'),log_file)
		os.system('gdal2tiles.py -z 20-22 ' + destination_map_path[index] + ' > ' + sysconf.createLogFile(project_name + '_' + mode + '_tiling.txt'))

		sysconf.writeLogRecord('executing tile folder transfer command : ' + 'cp -r ' + map_name[index] + ' ' + os.path.join('/'.join(destination_map_path[index].split('/')[:-1])),log_file)
		sysconf.writeLogRecord('executing original tile folder removal command : ' + 'rm -r ' + map_name[index],log_file)
		os.system('cp -r ' + map_name[index]+ ' ' + os.path.join('/'.join(destination_map_path[index].split('/')[:-1])))
		os.system('rm -r ' + map_name[index])

		sysconf.writeLogRecord('Tile path : ' + destination_map_path[index],log_file)
		if mode == 'ndvi':
			sysconf.writeLogRecord('##################################################################',log_file)
		tile_path.append(os.path.join('http://localhost',destination_map_path[index].split('htdocs/')[1].split('.tif')[0]))
	return {'mode':mode,'path':str(tile_path)}
