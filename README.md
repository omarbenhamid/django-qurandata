# django-qurandata
Tanzil.net quran corpus as django plugin

The data is preloaded during migration and can be accessed using the django model.

# Getting started

1. Install this app
```
$ git clone https://github.com/omarbenhamid/django-qurandata
$ cd django-qurandata
$ pip install -e .
```
2. Add it to INSTALLED_APPS of your application.
3. Now you can use the data. To test, go to your app directory :
```
$ python manage.py shell
Python 3.6.2 |Continuum Analytics, Inc.| (default, Jul 20 2017, 12:30:02) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from qurandata.models import *
>>> Sura.objects.first()
<Sura: (1) الفاتحة>
>>> list(_.aya_set.all())
[<Aya: (1:1) بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ>, 
<Aya: (1:2) الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ>, 
<Aya: (1:3) الرَّحْمَنِ الرَّحِيمِ>, 
<Aya: (1:4) مَالِكِ يَوْمِ الدِّينِ>, 
<Aya: (1:5) إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ>, 
<Aya: (1:6) اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ>, 
<Aya: (1:7) صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ>]
```
