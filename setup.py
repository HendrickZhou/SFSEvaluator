from setuptools import setup

install_requires=[
    'llist==0.7.1',
    # 'matlabengineforpython==9.13',
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