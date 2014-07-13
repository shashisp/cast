from django.db import models
import os.path



class File(models.Model):
	csvfile = models.FileField(upload_to='csvfiles/%Y/%m/%d')
	email = models.CharField(max_length=40)

	def __unicode__(self):
		return os.path.basename(self.csvfile.name)

