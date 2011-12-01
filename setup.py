import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Sudarmaa",
    version = "0.1",
    author = "Tulga",
    author_email = "sw06d103@gmail.com",
    description = ("Sudarmaa project"),
    license = "BSD",
    long_description=read('README'),
    install_requires=[
        'Django',
        'pinax',
        'django_debug_toolbar',
        'django_compressor',
        'django_staticfiles',
        'django_extensions',
        'PIL',
        'django-social-auth',
        'django-rosetta',
        'django-photologue',
    ],
)
