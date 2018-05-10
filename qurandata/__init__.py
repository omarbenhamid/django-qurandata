import re

class AyaRef:
    def __init__(self, reftxt, contextsura=None):
        m = re.match(r'(?:S(?P<sura>[0-9]+))?A(?P<startaya>[0-9]+)(?::A?(?P<endaya>[0-9]+))?',reftxt)
        self.startaya=int(m.group('startaya'))
        sura = m.group('sura')
        endaya = m.group('endaya')
        self.endaya = int(endaya) if endaya else self.startaya
        self.suraidx = int(sura) if sura else contextsura
    
    def isabsolute(self):
        return self.suraidx != None
    
    def count(self):
        return self.endaya - self.startaya + 1
    
    def getayas(self):
        if self.suraidx == None: raise Exception("Cannot get ayas of relative reference")
        return models.Aya.objects.filter(sura__index=self.suraidx, index__range=(self.startaya, self.endaya)).all()
    
def _parserefs(text, suraidx=None):
    ret = []
    for ref in re.findall(r'\b((?:S[0-9]+)?A[0-9]+(?::A?[0-9]+)?)\b','S2A1 S3A3, S4A4'):
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
    ayarefs = _parserefs(context)
    suraidx = ayarefs.pop() if len(ayarefs) > 0 else None
    return _parserefs(text, suraidx)
