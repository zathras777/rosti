from setuptools import setup
from os import path
import io

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='rosti',
    version='0.1',
    description='Script to clean nasty code from a compromised wordpress site.',
    long_description=long_description,
    url='https://github.com/zathras777/rosti',
    author='david reid',
    author_email='zathrasorama@gmail.com',
    license='Unlicense',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Video :: Display',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='appletv video ffmpeg streaming',
    entry_points={
        'console_scripts': ['rosti=rosti:main']
    },
    download_url = 'https://github.com/zathras777/rosti/tarball/0.1.0',
)
