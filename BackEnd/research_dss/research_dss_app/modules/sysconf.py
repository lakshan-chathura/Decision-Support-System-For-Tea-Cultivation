import os
from datetime import datetime

BASE_IMAGES_PATH = '/opt/lampp/htdocs' #'os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'
ODM_PATH = '~/Documents/Research/Tools/OpenDroneMap/'

def createLogFile(project_name):
    path = os.path.join(BASE_IMAGES_PATH,'data','logs',project_name + '.txt')
    if(os.path.exists(path) != True):
        os.system('touch ' + path)
    return path

def writeLogRecord(message,log_file):
    log_file.write('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + message + '\n')

def giveMapOrImagePath(map_or_image_type,project_name,image_name,data_type):
    folder_path = ''
    if(data_type == 'images'):
        folder_path = os.path.join(BASE_IMAGES_PATH,"data","images",(map_or_image_type + "_images"),project_name,'images')
    else:
        folder_path = os.path.join(BASE_IMAGES_PATH,"data","maps",(map_or_image_type + "_maps"),project_name)

    # folder_path = os.path.join(BASE_IMAGES_PATH,"data","maps",(map_type + "_maps"),project_name)

    if os.path.exists(folder_path) != True:
        os.system('mkdir -p ' + folder_path)

    if(data_type == 'images'):
        return folder_path
    else:
        return os.path.join(folder_path,image_name)

def getNDVIMapPath(project_name,image_name):
    return giveMapOrImagePath('ndvi',project_name,image_name,'map')
    # folder_path = os.path.join(BASE_IMAGES_PATH,"data","maps","ndvi_maps",project_name)
    # if os.path.exists(folder_path) != True:
    #     os.system('mkdir ' + folder_path)
    # return os.path.join(folder_path,image_name)

def getRGBMapPath(project_name,image_name):
    return giveMapOrImagePath('rgb',project_name,image_name,'map')
    # folder_path = os.path.join(BASE_IMAGES_PATH,"data","maps","rgb_maps",project_name)
    #
    # if os.path.exists(folder_path) != True:
    #     os.system('mkdir ' + folder_path)
    # return os.path.join(folder_path,image_name)

def getNIRMapPath(project_name,image_name):
    return giveMapOrImagePath('nir',project_name,image_name,'map')
    # folder_path = os.path.join(BASE_IMAGES_PATH,"data","maps","nir_maps",project_name)
    # if os.path.exists(folder_path) != True:
    #     os.system('mkdir ' + folder_path)
    # return os.path.join(folder_path,image_name)

def getNIRRawImagesPath(project_name):
    return giveMapOrImagePath('nir',project_name,'','images')
    # path = os.path.join(BASE_IMAGES_PATH,"data","images","nir_images",folder_name)
    # # os.system("mkdir " + path)
    # return path

def getRGBRawImagesPath(project_name):
    return giveMapOrImagePath('rgb',project_name,'','images')
    # path = os.path.join(BASE_IMAGES_PATH,"data","images","rgb_images",folder_name)
    # # os.system("mkdir " + path)
    # return path

def getNDVIPath(image_name):
    return os.path.join(BASE_IMAGES_PATH,"data","maps","ndvi_maps",image_name)

def getRGBRawMapPath(project_name):
    os.system('mkdir -p ' + os.path.join(BASE_IMAGES_PATH,"data","images","rgb_images",project_name))
    return os.path.join(BASE_IMAGES_PATH,"data","images","rgb_images",project_name,"odm_orthophoto","odm_orthophoto.original.tif")

def getNIRRawMapPath(project_name):
    os.system('mkdir -p ' + os.path.join(BASE_IMAGES_PATH,"data","images","nir_images",project_name))
    return os.path.join(BASE_IMAGES_PATH,"data","images","nir_images",project_name,"odm_orthophoto","odm_orthophoto.original.tif")

def getRGBGeoDataLogPath(folder_name,text_file_name):
    path = getRGBRawImagesPath(folder_name).split(folder_name)
    return os.path.join(path[0],folder_name,text_file_name)

def getNIRGeoDataLogPath(folder_name,text_file_name):
    path = getNIRRawImagesPath(folder_name).split(folder_name)
    return os.path.join(path[0],folder_name,text_file_name)

def getODMExecutablePath():
    return ODM_PATH

def getTeaBudIndetifiedMapPath(project_name,image_name):
    os.system('mkdir -p ' + os.path.join(BASE_IMAGES_PATH,"data","maps","rgb_maps",project_name,"modified"))
    return os.path.join(BASE_IMAGES_PATH,"data","maps","rgb_maps",project_name,"modified",image_name)
