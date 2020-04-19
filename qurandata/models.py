from django.db import models
import re
from _tracemalloc import start

class CachingSuraManager(models.Manager):
    
    def get(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 1 and 'index' in kwargs:
            if not hasattr(self,'_cache'):
                self._cache={}
                for sura in Sura.objects.all():
                    self._cache[getattr(sura,'index')]=sura
                
            return self._cache.get(kwargs['index'])
        else:
            return models.Manager.get(self, *args, **kwargs)
        

# Create your models here.
class Sura(models.Model):
    index = models.PositiveIntegerField()
    ayas = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    
    objects = CachingSuraManager()
    
    class Meta:
        ordering=['index']
    
    def __str__(self):
        return "(%d) %s" % (self.index,self.name)

class CachingAyaManager(models.Manager):
    
    def _check_cache(self):
        if hasattr(self,'_cache'): return
        ayas = list(Aya.objects.select_related('sura')\
                        .order_by('sura__index','index'))
        self._page_cache={}
        for aya in ayas:
            if aya.page not in self._page_cache:
                self._page_cache[aya.page]=[]
            self._page_cache[aya.page].append(aya)
        
        self._cache={}
        for aya in ayas:
            self._cache[(aya.sura.index, aya.index)]=aya
                    
    def list_by_page(self, page):
        self._check_cache()    
        return self._page_cache[page]
        
    def get_by_index(self, sura_index, index):
        self._check_cache()    
        return self._cache.get((sura_index, index))
        
class Aya(models.Model):
    sura = models.ForeignKey(Sura, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()
    text = models.TextField()
    page = models.PositiveIntegerField("Page in madani quran")
    
    objects = CachingAyaManager()
    
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
    