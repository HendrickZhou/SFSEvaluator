"""
this script serves as a singleton matlab engine for all the scripts across this project

@Author: Hang Zhou
"""

import matlab
import matlab.engine

first=True
_the_one_and_only_eng=None

def get_eng():
    global first
    if first:
        global _the_one_and_only_eng
        print("engine starting")
        _the_one_and_only_eng=matlab.engine.start_matlab()
        first=False
        return _the_one_and_only_eng
    print("engine started")
    return _the_one_and_only_eng