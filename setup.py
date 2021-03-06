import os
from setuptools import setup, find_packages


README = "Quran data for django"

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),
                                       os.pardir)))

requirements = [
    'django>=1.5',
]

extras_require = {
    'test': [],
}

setup(
    name='django-qurandata',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    license='Public Domain',
    description='A django application to add Quran Data.',
    long_description=README,
    url='https://github.com/omarbenhamid/django-qurandata',
    author='Omar BENHAMID',
    author_email='contact@obenhamid.me',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
