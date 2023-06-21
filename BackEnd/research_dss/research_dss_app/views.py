from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from research_dss_app.models import FieldVisit,PlantHealth
from research_dss_app.serializers import FieldVisitSerializer,PlantHealthSerializer
from research_dss_app.modules.ndvi_module import ndvi_module
from research_dss_app.modules.mapping_module import mapping_module
from research_dss_app.modules.tea_bud_identification_module import tea_bud_identification_module
from research_dss_app.modules import sysconf
import os,time,json
from datetime import datetime
# Create your views here.
"""
Handles the NDVI module. Inputs are the NIR and RGB map names.
Request type should be PUT and the output of this put method in this view class
is the percentage of plants with good health and bad health, non plant percentage
and the NDVI map name.
"""
class NDVIMapView(APIView):
    def post(self,request,format=None):
        f = open(sysconf.createLogFile(request.data['project_name']),"a+")
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "Started the NDVI module")
        sysconf.writeLogRecord('NDVI analysis is started',f)
        #sysconf.writeLogRecord('Request data : ' + json.dumps(request.data))
        sysconf.writeLogRecord('NDVI red, green and blue layer maps generation started',f)
        NDVI_MAP_PATH = sysconf.getNDVIMapPath(request.data['project_name'],'ndvi_map_final')
        sysconf.writeLogRecord('NDVI map path : ' + NDVI_MAP_PATH,f)
        sysconf.writeLogRecord('RGB map : ' + sysconf.getRGBMapPath(request.data['project_name'],'rgb_map_final.tif'),f)
        sysconf.writeLogRecord('NIR map : ' + sysconf.getNIRMapPath(request.data['project_name'],'nir_map_final.tif'),f)
        # print("Creating the NDVI red, green and blue layer maps",end="")
        # request.data['nir_map_name'] should be 'nir_map'
        # request.data['rgb_map_name'] should be 'rgb'_map'
        NDVI_MAP = ndvi_module.createNDVIMap(
            sysconf.getNIRMapPath(request.data['project_name'],'nir_map_final.tif'),#,request.data['nir_map_name']),
            sysconf.getRGBMapPath(request.data['project_name'],'rgb_map_final.tif'),#request.data['rgb_map_name']),
            NDVI_MAP_PATH,f
            )
        # print("......done")
        sysconf.writeLogRecord('NDVI red, green and blue layer maps generation complete',f)
        sysconf.writeLogRecord('Plant health analysis is started',f)
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "Calculating the plant health analysis",end="")
        HEALTH_ANALYSIS = ndvi_module.calculateHealthyAndNonHealthyPlantPercentage(NDVI_MAP)
        print("......done")
        sysconf.writeLogRecord('Plant health analysis is complete',f)
        sysconf.writeLogRecord('Georeferencing NDVI red, green and blue layer maps is started',f)
        mapping_module.createGeoTiff(request.data['project_name'], 'ndvi',f)
        sysconf.writeLogRecord('Georeferencing NDVI red, green and blue layer maps is completed',f)
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "Saving data in the database",end="")
        sysconf.writeLogRecord('Saving the data to database is started',f)
        fieldVisit = FieldVisit.objects.get(real_name=request.data['project_name'])
        plantHealthSerializer = PlantHealthSerializer(data={'project_id':fieldVisit.id,'good_plant_health':HEALTH_ANALYSIS['Good_health'],'bad_plant_health':HEALTH_ANALYSIS['Bad_health'],'non_plants':HEALTH_ANALYSIS['Non_plants']})
        if(plantHealthSerializer.is_valid()):
            plantHealthSerializer.save()
            sysconf.writeLogRecord('Saving the data to database is complete',f)
        sysconf.writeLogRecord('DB Object errors : ' + str(plantHealthSerializer.errors),f)
        sysconf.writeLogRecord('NDVI analysis is complete',f)
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'NDVI module is Finished')
        f.close()
        # print("......done")
        return Response({'results':HEALTH_ANALYSIS,'path':NDVI_MAP_PATH})

"""
Handles the mapping module. The request type should be GET. No inputs required.
It outputs the path of the NIR and RGB map
"""
class RGBAndNIRMapView(APIView):
    def post(self,request,operation,format=None):
        # rgbMap = 'IMG_8764_RGB.jpg'
        # nirMap = 'IMG_8763_RGB.jpg'
        # resultantRGBMap = 'RGB_Ortho.jpg'
        # resultantNIRMap = 'NIR_Ortho.jpg'
        if(operation == 'geotag'):
            f = open(sysconf.createLogFile(request.data['project_name']),"a+")
            #Geotag nir_images
            sysconf.writeLogRecord('NIR image geotagging has been started.',f)
            #sysconf.writeLogRecord('Request data : ' + json.dumps(request.data))
            print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "Geotagging NIR images",end="")
            mapping_module.geotagging_images(request.data['project_name'],f)
            print("......done")
            sysconf.writeLogRecord('NIR images geotagging is complete.',f)
            f.close()
            return Response({'message':'geotagging is complete'})
        if(operation == 'mapping'):
            #Create orthomosaics
            f = open(sysconf.createLogFile(request.data['project_name']),"a+")
            sysconf.writeLogRecord('orthomosaic generation started',f)
            #sysconf.writeLogRecord('Request data : ' + json.dumps(request.data))
            print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + "When orthomosaics are generating an new terminal will execute the task and the server terminal might look like unresponsive. But don't panic. It's on the way.")
            mapping_module.Create_Orthomap(request.data['project_name'],request.data['mode'],f)
            print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + request.data['mode'] + 'mapping is done')
            # if(request.data['mode'] == 'rgb'):
            #     print('RGB mapping......done')
            #     mapping_module.Create_Orthomap(request.data['project_name'],'rgb')
            # else:
            #     print('NIR mapping......done')
            #     mapping_module.Create_Orthomap(request.data['project_name'],'nir')
            sysconf.writeLogRecord('orthomosaic generation completed',f)
            f.close()
            return Response({'message':request.data['mode'] + ' orthomosaic generation is complete'})
            #Create NIR map

        if(operation == 'align'):
            f = open(sysconf.createLogFile(request.data['project_name']),"a+")
            sysconf.writeLogRecord('Aligning images has been started',f)
            #sysconf.writeLogRecord('Request data : ' + json.dumps(request.data))
            sysconf.writeLogRecord("Raw RGB map : " + sysconf.getRGBRawMapPath(request.data['project_name']),f)
            sysconf.writeLogRecord("Raw NIR map : " + sysconf.getNIRRawMapPath(request.data['project_name']),f)
            sysconf.writeLogRecord("Resultant RGB map : " + sysconf.getRGBMapPath(request.data['project_name'],'rgb_map_final.png'),f)
            sysconf.writeLogRecord("Resultant NIR map : " + sysconf.getNIRMapPath(request.data['project_name'],'nir_map_final.png'),f)
            #Overlap the maps
            print("Aligning images",end="")
            print("Raw RGB map : " + sysconf.getRGBRawMapPath(request.data['project_name']))
            print("Raw NIR map : " + sysconf.getNIRRawMapPath(request.data['project_name']))
            print("Resultant RGB map : " + sysconf.getNIRMapPath(request.data['project_name'],'rgb_map_final.png'))
            print("Resultant NIR map : " + sysconf.getNIRMapPath(request.data['project_name'],'nir_map_final.png'))

            resultantOverlappedNIRMap = mapping_module.Image_Overlap(sysconf.getRGBRawMapPath(request.data['project_name']),sysconf.getNIRRawMapPath(request.data['project_name']),sysconf.getNIRMapPath(request.data['project_name'],'nir_map.png'),f)
            resultantOverlappedRGBMap = mapping_module.Image_Overlap(sysconf.getNIRRawMapPath(request.data['project_name']),sysconf.getRGBRawMapPath(request.data['project_name']),sysconf.getRGBMapPath(request.data['project_name'],'rgb_map.png'),f)
            # resultantOverlappedNIRMap = mapping_module.Image_Overlap(sysconf.getRGBRawMapPath(request.data['project_name']),sysconf.getNIRRawMapPath(request.data['project_name']),sysconf.getNIRMapPath(request.data['project_name'],'nir_map.jpg'))
            # resultantOverlappedRGBMap = mapping_module.Image_Overlap(sysconf.getNIRRawMapPath(request.data['project_name']),sysconf.getRGBRawMapPath(request.data['project_name']),sysconf.getRGBMapPath(request.data['project_name'],'rgb_map.jpg'))

            sysconf.writeLogRecord('Georeferencing RGB map image started',f)
            mapping_module.createGeoTiff(request.data['project_name'], 'rgb',f)
            sysconf.writeLogRecord('Georeferencing RGB map image completed',f)
            sysconf.writeLogRecord('Georeferencing NIR map image started',f)
            mapping_module.createGeoTiff(request.data['project_name'], 'nir',f)
            sysconf.writeLogRecord('Georeferencing NIR map image completed',f)
            #mapping_module.createGeoTiff(sysconf.getNIRRawMapPath(request.data['project_name']),sysconf.getNIRMapPath(request.data['project_name'],'nir_map_final.png'))
            #mapping_module.createGeoTiff(sysconf.getNDVIMapPath(request.data['project_name']),sysconf.getNIRMapPath(request.data['project_name'],'nir_map_final.png'))
            sysconf.writeLogRecord('orthomosaic aligning is complete',f)
            f.close()
            return Response({'message':'Alligning is complete','rgb_map':resultantOverlappedRGBMap,'nir_map':resultantOverlappedNIRMap})
            # os.system('rm -r ' + sysconf.getRGBMapPath(rgbMap))
            # os.system('rm -r ' + sysconf.getNIRMapPath(nirMap))
            print("......done")

"""
This view class responsible for tea bud identification. Still constructing
"""
class TeaBudIdentificationView(APIView):
    def post(self,request,format=None):
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Tea buds identification is started')
        f = open(sysconf.createLogFile(request.data['project_name']),"a+")
        sysconf.writeLogRecord('Tea bud identification process is started',f)
        tea_bud_identification_module.analyzeTeaBuds(request.data['project_name'],f)
        sysconf.writeLogRecord('Georeferencing RGB cluster map image started',f)
        mapping_module.createGeoTiff(request.data['project_name'], 'cluster',f)
        sysconf.writeLogRecord('Georeferencing RGB cluster map image started',f)
        sysconf.writeLogRecord('Tea bud identification process is complete',f)
        f.close()
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Tea buds identification is finished')
        # request.data['rgb_map'] should be 'rgb_map' because the name is static
        return Response({'nir_path':sysconf.getTeaBudIndetifiedMapPath(request.data['project_name'],'rgb_processed.jpg')})

"""
Responsible for retrieving the data in the DB.
"""
class FieldVisitView(APIView):
    def get(self,request,format=None):
        plantHealthSerializer = PlantHealthSerializer(PlantHealth.objects.all().prefetch_related('project_id'), many=True)
        for item in plantHealthSerializer.data:
            fieldVisitObj = FieldVisitSerializer(FieldVisit.objects.get(id=item['project_id']))
            item['project_data'] = fieldVisitObj.data
        return Response({'data':plantHealthSerializer.data})

    def put(self,request,real_name,mode,format=None):
        f = open(sysconf.createLogFile(real_name),"a+")
        sysconf.writeLogRecord('Uploading ' + mode + ' images started',f)
        fieldVisitObj = FieldVisit.objects.get(real_name=real_name)
        #sysconf.writeLogRecord('Request data : ' + request.body.decode('utf-8'))
        path = ''
        if mode == 'rgb':
            path = sysconf.getRGBRawImagesPath(fieldVisitObj.real_name)
        else:
            path = sysconf.getNIRRawImagesPath(fieldVisitObj.real_name)

        for count, x in enumerate(request.FILES.getlist("images[]")):
            def process(f):
                with open(path + '/img_' + str(count) + '.JPG', 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            process(x)
        sysconf.writeLogRecord('Uploading ' + mode + ' images completed',f)
        f.close()
        return Response("File(s) uploaded!")

class TilerView(APIView):
    def put(self,request,format=None):
        #odm_orthophoto.original.tiff should be replaced by 'nir_map' and 'rgb_map'
        #because they already created
        f = open(sysconf.createLogFile(request.data['project_name']),"a+")
        sysconf.writeLogRecord('Tile generation is started',f)
        #sysconf.writeLogRecord('Request data : ' + json.dumps(request.data))
        response = mapping_module.createTiles(request.data['project_name'],request.data['mode'],f)
        sysconf.writeLogRecord('Tile generation is complete',f)
        f.close()
        return Response({'response':response})

    def post(self,request,format=None):
        real_project_name = request.data['project_name'] + '_' + str(int(round(time.time() * 1000)))
        f = open(sysconf.createLogFile(real_project_name),"w+")
        sysconf.writeLogRecord('Inserting project data to the database.',f)
        # sysconf.writeLogRecord('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] Inserting project data to the database')
        # millis = int(round(time.time() * 1000))
        fieldVisitObj = FieldVisitSerializer(data={'name':request.data['project_name'],'real_name':real_project_name})
        #sysconf.writeLogRecord('Request data ' + json.dumps(request.data))
        sysconf.writeLogRecord('Project real name is ' + real_project_name + '.',f)
        sysconf.writeLogRecord('Saving project database object in database.',f)
        #sysconf.writeLogRecord('DB object : ' + json.dumps(fieldVisitObj))
        sysconf.writeLogRecord('Serailizer : FieldVisitSerializer',f)
        if fieldVisitObj.is_valid():
            fieldVisitObj.save()
            sysconf.writeLogRecord('DB object saved successfully',f)
        sysconf.writeLogRecord('Erros in DB object : ' + str(fieldVisitObj.errors),f)
        sysconf.writeLogRecord('Response : ' + json.dumps({'project_real_name':real_project_name}),f)
        sysconf.writeLogRecord('Project data insertion to database is complete',f)
        f.close()
        return Response({'project_real_name':real_project_name})
