""" IO utility
standard IO tools for the database objects
So far three different kinds of file are supported
.mat file(could be image)
image file(all)

@Author: Hang Zhou
"""

from enum import Enum,auto
from matlab_agent import get_eng
from exception import *
import matlab
from math import isnan,nan
from PIL import Image
import numpy as np

class FileType(Enum):
    MAT=auto()
    IMG=auto()

class DataType(Enum):
    NUMPY=auto()
    MATLAB=auto()

def get_image(file_path:str, file_type:FileType, my_type:FileType)->any:
    """get image from file_type to my_type"""
    if(file_path==None):
        return None
    if file_type is FileType.IMG:
        if my_type is DataType.MATLAB:
            eng=get_eng()
            try:
                img=eng.imread(file_path)
            except Exception as e:
                raise InvalidResourceError from e
            else:
                return img
        elif my_type is DataType.NUMPY:
            try:
                Image.open(file_path)
            except Exception as e:
                raise InvalidResourceError from e
            else:
                return np.array()
        else:
            print("unsupported image type")
            raise IllegalTypeError
    elif file_type is FileType.MAT:
        if my_type is DataType.MATLAB:
            try:
                img=eng.get_mat(file_path)
            except AssertionError as e:
                raise WrongFormatError from e
            except InvalidResourceError:
                raise
            else:
                return img 
        elif my_type is DataType.NUMPY:
            try:
                mat=get_mat(file_path)
                img=mat2np2d(mat)
            except AssertionError as e:
                raise WrongFormatError from e
            except InvalidResourceError:
                raise
            else:
                return img
        else:
            raise IllegalTypeError
    else:
        raise IllegalTypeError

def get_mat(file_path:str):
    """load the mat file to a matlab object
    Assume there's only one variable in this mat file!
    Will also assume it's a double matrix type
    """
    if file_path is None:
        return None
    
    eng=get_eng()
    try:
        ret=eng.load(file_path)
    except Exception as e:
        raise InvalidResourceError from e
    
    _,sth=ret.popitem()
    assert type(sth) is matlab.double, f"mat file contains double matrix expetec, got: {type(sth)}"
    return sth

def mat2np3d(mat:matlab.double)->np.array:
    """convert 3d matlab matrix to numpy 2d array"""
    if mat is None:
        return None
    eng=get_eng()
    size_mat=eng.size(mat)
    w=int(size_mat[0][0])
    h=int(size_mat[0][1])
    c=int(size_mat[0][2])
    result=np.zeros((w,h,c))
    for i in range(w):
        for j in range(h):
            for k in range(c):
                the_val=mat[i][j][k]
                if isnan(the_val):
                    continue
                result[i][j][k]=the_val
    return result 

def mat2np2d(mat:matlab.double)->np.array:
    """convert 2d matlab matrix to numpy 2d array"""
    if mat is None:
        return None
    eng=get_eng()
    size_mat=eng.size(mat)
    w=int(size_mat[0][0])
    h=int(size_mat[0][1])
    result=np.zeros((w,h))
    for i in range(w):
        for j in range(h):
            the_val=mat[i][j]
            if isnan(the_val):
                continue
            result[i][j]=the_val
    return result

def NANfy(input):
    if input is None:
        return nan
    return input