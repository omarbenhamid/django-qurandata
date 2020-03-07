from django.db import models
import re
from _tracemalloc import start

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
    page = models.PositiveIntegerField("Page in madani quran")
    
    class Meta:
        ordering=['sura','index']
    
    def get_url(self, mushaf="hafs"):
        return "http://quran.ksu.edu.sa/index.php#aya=%d_%d&m=%s" % (self.sura.index, self.index, mushaf)
    
    def get_audio_url(self):
        #return "http://everyayah.com/data/Ayman_Sowaid_64kbps/%03d%03d.mp3" % (self.index, self.sura.index)
        return "http://cdn.ksu.edu.sa/quran/ayat/mp3/Ayman_Sowaid_64kbps/%03d%03d.mp3" % (self.sura.index, self.index)
    
    def __str__(self):
        return "(%d:%d) %s" % (self.sura.index, self.index,self.text)
    
class Quarter(models.Model):
    index = models.PositiveIntegerField("Global position of quarter")
    hizb = models.PositiveIntegerField("Index of hizb")
    pos_in_hizb = models.PositiveIntegerField("Posiiton in hizb : 1 to 4")
    
    startaya = models.ForeignKey(Aya, related_name='+', on_delete=models.CASCADE)
    endaya = models.ForeignKey(Aya, related_name='+', on_delete=models.CASCADE)
    