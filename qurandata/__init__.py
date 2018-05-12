import re

class AyaRef:
    def __init__(self, reftxt, contextsura=None):
        m = re.match(r'^(?:S(?P<singlesura>[0-9]+)|(?:S(?P<sura>[0-9]+))?A(?P<startaya>[0-9]+)(?::A?(?P<endaya>[0-9]+))?)$',reftxt)
        self.expr = reftxt
        ssura = m.group('singlesura')
        if ssura:
            self.fullsura = True
            self.suraidx = int(ssura)
            self.startaya = 1
            self._endaya = None
            return
        self.fullsura = False
        sura = m.group('sura')
        self.suraidx = int(sura) if sura else contextsura
        self.startaya=int(m.group('startaya'))
        endaya = m.group('endaya')
        self._endaya = int(endaya) if endaya else self.startaya
        
    def __repr__(self):
        if self.fullsura:
            return '<AyaRef %s (sura %r)>' % (self.expr, self.suraidx)
        else:
            return "<AyaRef %s (sura %r, ayas %r-%r)>" % (self.expr, self.suraidx, self.startaya, self._endaya)
    
    @property
    def endaya(self):
        if self._endaya == None and self.suraidx:
            self._endaya = models.Sura.objects.get(index=self.suraidx).ayas
        return self._endaya
    
    def isabsolute(self):
        return self.suraidx != None
    
    def count(self):
        return self.endaya - self.startaya + 1
    
    def getayas(self):
        if self.suraidx == None: raise Exception("Cannot get ayas of relative reference")
        return models.Aya.objects.filter(sura__index=self.suraidx, index__range=(self.startaya, self.endaya)).all()
    
    def ashtml(self):
        if self.fullsura:
            return '<span dir="rtl" title="%s">%s</span>' % (self.expr,
                models.Sura.objects.get(index=self.suraidx).name)
        else:
            return '<span dir="rtl" title="%s">%s من <span class="citation">%d</span> إلى <span class="citation">%d</span></span>' % (self.expr,
                models.Sura.objects.get(index=self.suraidx).name if self.suraidx else '',
                self.startaya, self.endaya)
    
    
    def astext(self):
        if self.fullsura:
            return models.Sura.objects.get(index=self.suraidx).name
        else:
            return '%s من %d إلى %d' % (models.Sura.objects.get(index=self.suraidx).name if self.suraidx else '',
                self.startaya, self.endaya)
    
def _parserefs(text, suraidx=None):
    ret = []
    for ref in re.findall(r'\b(S[0-9]+|(?:S[0-9]+)?A[0-9]+(?::A?[0-9]+)?)\b',text):
        r = AyaRef(ref, contextsura=suraidx)
        if not r.isabsolute(): continue
        ret.append(r)
        suraidx = r.suraidx
    
    return ret

def refs_from_text(text, context=""):
    """
        Parses ayarange reference and returns an Ayaref object for each.
        Referances in text are in the format :
        [S?]A?[:[A]?], this means : 
            - S1A2 is surah 1 ayah 2
            - A3 is aya 3 of last surah identified in text (or in contexttext)
            - S1A2:5 or S1A2:A5 is ayat form aya 2 to aya 5 of surah 1
    """
    if context==None: context=""
    ayarefs = _parserefs(context)
    suraidx = ayarefs.pop() if len(ayarefs) > 0 else None
    return _parserefs(text, suraidx)
