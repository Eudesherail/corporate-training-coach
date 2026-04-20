from django.db import models

class AdminDocuments(models.Model):
    name = models.CharField(max_length = 255)
    filePath = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    modul = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    userName = models.CharField(max_length=255,null=True)


    def __str__(self):
        return self.institution + ' - ' + self.name
