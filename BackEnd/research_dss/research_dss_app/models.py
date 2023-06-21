from django.db import models

# Create your models here.
class FieldVisit(models.Model):
    real_name = models.CharField(max_length=100,null=False,blank=False)
    name = models.CharField(max_length=100,null=False,blank=False)
    date = models.DateField(auto_now_add=True,blank=False)
    time = models.TimeField(auto_now_add=True,blank=False)
    # rgb_map = models.CharField(max_length=50,null=False,blank=False)
    # nir_map = models.CharField(max_length=50,null=False,blank=False)
    # ndvi_map = models.CharField(max_length=50,null=True,blank=True)
    # tile_location = models.CharField(max_length=50,null=False,blank=False)

    # class Meta:
    #     managed = True
    #     db_table = 'PlantHealths'

    def __str__(self):
        return self.name + ' ' + str(self.date) + ' ' + str(self.time)

class PlantHealth(models.Model):
    project_id = models.ForeignKey('FieldVisit',on_delete=models.CASCADE)
    good_plant_health = models.FloatField(null=False,blank=False)
    bad_plant_health = models.FloatField(null=False,blank=False)
    non_plants = models.FloatField(null=False,blank=False)
    # ndvi_map_test = models.ForeignKey('FieldVisit',on_delete=models.CASCADE)

    # class Meta:
    #     managed = True
    #     db_table = 'FieldVisits'

    def __str__(self):
        return self.project_id.name
