"""
this script serves as a singleton matlab engine for all the scripts across this project

@Author: Hang Zhou
"""

import matlab
import matlab.engine


_the_one_and_only_eng=None
first=True

def get_eng():
    if first:
        global _the_one_and_only_eng
        _the_one_and_only_eng=matlab.engine.start_matlab()
        first=False
    return _the_one_and_only_eng