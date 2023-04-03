from setuptools import setup

import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
with open(requirement_path) as f:
    install_requires = list(f.read().splitlines())

install_requires=[
    'llist==0.7.1',
    'matlabengineforpython==9.13',
    'open3d==0.16.1',
    'openpyxl==3.1.2',
    'Pillow==9.4.0',
    'numpy==1.24.2',
]
setup(
    name='sfseval',
    install_requires=install_requires,
    packages=['sfseval','sfseval.CBM','sfseval.DSM'],
    entry_points={
        
    },
)