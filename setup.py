from setuptools import setup

import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
with open(requirement_path) as f:
    install_requires = list(f.read().splitlines())
setup(
    name='sfseval',
    install_requires=install_requires,
    packages=['sfseval','sfseval.CBM','sfseval.DSM'],
    entry_points={
        
    },
)