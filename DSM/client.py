'''
author: Hang Zhou

sending the request to register the dataset and pull the dataset object
'''

import socket
from rdataset import *

# send decorator
def SEND():
    pass
# get decorator
def GET():
    pass


'''
$ dsm reg -path -name -descriptor
'''
@SEND
def send_reg(path,name,descriptor):
    rd=ReconDataset()
    rd._register(path, name, descriptor)
    # send sobj

'''
$ dsm ls
'''
@GET
def get_ls():
    pass

'''
$ dataset=dataset.get(id)
'''
@GET
def get_data(name, id):
    # get obj over protocol
    # sobj=
    sobj=None
    return sobj.deserialize()


