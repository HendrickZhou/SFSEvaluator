import os

# ondir must contains / in the end
def create_dir(ondir, name):
    abs_name=ondir+name
    if not os.path.isdir(abs_name):
         os.makedirs(abs_name)
         return abs_name
    else:
        return abs_name
        
def display_mat():
    pass
# def create_file(path, name):
#     if not os.

def Print(msg):
    print("********************")
    print("* "+msg)
    print("********************")

def breaker():
    print("********************")
