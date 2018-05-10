from django.db import models
import re

# Create your models here.

class Sura(models.Model):
    index = models.PositiveIntegerField()
    ayas = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering=['index']
    
    def __str__(self):
        return "(%d) %s" % (self.index,self.name)

class Aya(models.Model):
    sura = models.ForeignKey(Sura, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    text = models.TextField()
    
    class Meta:
        ordering=['sura','index']
    
    def get_url(self, mushaf="hafs"):
        return "http://quran.ksu.edu.sa/index.php#aya=%d_%d&m=%s" % (self.sura.index, self.index, mushaf)
    
    
    def __str__(self):
        return "(%d:%d) %s" % (self.sura.index, self.index,self.text)