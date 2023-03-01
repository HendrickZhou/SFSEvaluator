'''
author: Hang Zhou

handling the request to register & get the dataset
support local transfer
but extentable to remote architecture

api works around the _DSM object that manage everything
'''

import socket
from rdataset import _SObj


config={
    "store_path":None
}
'''
$ dsm up
init server and connect to the database/files
'''
def start_server():
    pass

'''
$ dsm config
configuration: path to store the dataset obj etc
can be extended to support database as backend
'''
def config(path):
    config["store_path"]=path

def receive(s_obj:_SObj):
    pass

def respond():
    pass


class _DSM():
    def register():
