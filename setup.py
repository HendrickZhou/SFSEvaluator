from setuptools import setup

install_requires=[
    'llist==0.7.1',
    # 'matlabengineforpython==9.13',
    'openpyxl==3.1.2',
    'Pillow==9.4.0',
    'numpy',
]
setup(
    name='sfseval',
    install_requires=install_requires,
    packages=['sfseval','sfseval.CBM','sfseval.DSM'],
    entry_points={
        
    },
)