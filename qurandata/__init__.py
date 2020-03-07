import re

class BadRef(Exception):
    def __init__(self, ref, errcode):
        self.ref = ref
        self.errcode = errcode
        
    def __str__(self):
        return 'Bad Aya Ref %s : %s' % (self.ref, self.errcode)

class AyaRef:
    def __init__(self, reftxt, contextsura=None, validate=True, sura=None, firstaya=None, endaya=None, label=None):
        self.expr = reftxt
        self.label = label
        if sura==None: 
            self.__init_from_reftxt(reftxt, contextsura)
        else:
            self.fullsura = (firstaya==None and endaya==None)
            self.suraidx = sura
            self.startaya = 1 if firstaya== None else firstaya
            self._endaya = endaya
            
        if validate: self.validate()
            
    def __init_from_reftxt(self, reftxt, contextsura=None):
        m = re.match(r'^(?:S(?P<singlesura>[0-9]+)|(?:S(?P<sura>[0-9]+))?A(?P<startaya>[0-9]+)(?::A?(?P<endaya>[0-9]+))?)$',reftxt, flags=re.I)
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
        
    def validate(self):
        if self.startaya <= 0:
            raise BadRef(self.expr, 'bat-start-aya-index')
        
        if self.endaya < self.startaya:
            raise BadRef(self.expr, 'end-aya-less-than-start-aya')
            
        if self.suraidx == None: 
            return
        
        try:
            sura = models.Sura.objects.get(index=self.suraidx)
        except:
            raise BadRef(self.expr, 'sura-not-found')
        
        if self.startaya > sura.ayas:
            raise BadRef(self.expr, 'start-aya-not-in-sura')
        if self.endaya > sura.ayas:
            raise BadRef(self.expr, 'end-aya-not-in-sura')
        
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
        if self.label:
            return '<span dir="rtl" title="%s">%s</span>' % (self.expr,
                self.label)
        elif self.fullsura:
            return '<span dir="rtl" title="%s">%s</span>' % (self.expr,
                models.Sura.objects.get(index=self.suraidx).name)
        else:
            return '<span dir="rtl" title="%s">%s من <span class="citation">%d</span> إلى <span class="citation">%d</span></span>' % (self.expr,
                models.Sura.objects.get(index=self.suraidx).name if self.suraidx else '',
                self.startaya, self.endaya)
    
    
    def astext(self):
        if self.label:
            return self.label
        elif self.fullsura:
            return models.Sura.objects.get(index=self.suraidx).name
        else:
            return '%s من %d إلى %d' % (models.Sura.objects.get(index=self.suraidx).name if self.suraidx else '',
                self.startaya, self.endaya)

def parse_hizbrefs(text):
    HRREGEX=r'\b(H(?P<singlehizb>[0-9]+)|H(?P<nisfhizb>[0-9]+)N(?P<nisfnum>[1-2])|H(?P<quarterhizb>[0-9]+)R(?P<quarternum>[1-4]))\b'
    for m in re.finditer(HRREGEX,text, flags=re.I):
        if m.group('singlehizb'):
            hizb = int(m.group('singlehizb'))
            label='ح%d - '%hizb
            minq=1+(hizb-1)*4
            maxq=minq+3
        elif m.group('nisfhizb'):
            hizb = int(m.group('nisfhizb'))
            nisf = int(m.group('nisfnum'))
            label='ح%dن%d - '%(hizb,nisf)
            minq=1+(hizb-1)*4+(nisf-1)*2
            maxq=minq+1
        elif m.group('quarterhizb'):
            hizb = int(m.group('quarterhizb'))
            quart = int(m.group('quarternum'))
            label='ح%dر%d - '%(hizb,quart)
            minq=1+(hizb-1)*4+(quart-1)
            maxq=minq
        q=list(models.Quarter.objects.filter(index__in=(minq,maxq)).order_by('index').all())
        firstq=q[0]
        lastq=q[-1]
        label += ' '.join(firstq.startaya.text.split(maxsplit=2)[0:2])
        firstsura=firstq.startaya.sura
        lastsura=lastq.endaya.sura
        label += '... (%s ص%d)' % (firstsura.name, firstq.startaya.page)
        for s in range(firstsura.index, lastsura.index+1):
            if s not in (firstsura.index, lastsura.index):
                yield AyaRef(reftxt=m.group(), label=label, sura=s)
                continue
            if s==firstsura.index:
                if s==lastsura.index:
                    #If start and end in same sura use endaya of last quarter.
                    endaya=lastq.endaya.index
                else:
                    endaya = firstsura.ayas
                    
                yield AyaRef(reftxt=m.group(), label=label, sura=s, firstaya=q[0].startaya.index, endaya=endaya, validate=False)
                continue
            if s==lastsura.index:
                #this implcitly means the lastsura !=firstsura or last if would have matched.
                yield AyaRef(reftxt=m.group(), label=label, sura=s, firstaya=1, endaya=lastq.endaya.index, validate=False)
            

def _parserefs(text, suraidx=None, ignoreinvalid=True):
    ret = []
    for ref in re.findall(r'\b(S[0-9]+|(?:S[0-9]+)?A[0-9]+(?::A?[0-9]+)?)\b',text, flags=re.I):
        r = AyaRef(ref, contextsura=suraidx, validate=False)
        try:
            r.validate()
        except:
            if ignoreinvalid: continue
            else: raise
        if not r.isabsolute(): continue
        ret.append(r)
        suraidx = r.suraidx
    
    return ret

def refs_from_text(text, context="", ignoreinvalid=True):
    """
        Parses ayarange reference and returns an Ayaref object for each.
        Referances in text are in the format :
        [S?]A?[:[A]?], this means : 
            - S1A2 is surah 1 ayah 2
            - A3 is aya 3 of last surah identified in text (or in contexttext)
            - S1A2:5 or S1A2:A5 is ayat form aya 2 to aya 5 of surah 1
            
        ignoreinvalid is true by default, invalid aya ranges are silently ingored.
        When set to false, they provoque a BadRef exception if an invalid ayaref is encountred.
    """
    if context==None: context=""
    #Ignore invalid refs when parsing context
    ayarefs = _parserefs(context, ignoreinvalid=True)
    suraidx = ayarefs.pop().suraidx if len(ayarefs) > 0 else None
    ret = _parserefs(text, suraidx, ignoreinvalid=ignoreinvalid)
    ret.extend(parse_hizbrefs(text))
    return ret
