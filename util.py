import os

def create_dir(ondir=None, name=None,abs_name=None):
    """ondir must contains / in the end"""
    if abs_name is None:
        abs_name=ondir+name
    if not os.path.isdir(abs_name):
         os.makedirs(abs_name)
         return abs_name
    else:
        return abs_name

def file_exist(ondir=None,name=None,abs_name=None):
    if abs_name is None:
        abs_name=ondir+name
    if not os.path.isfile(abs_name):
        return False
    return True
       
def Print(msg):
    print("********************")
    print("* "+msg)
    print("********************")

def breaker():
    print("********************")
