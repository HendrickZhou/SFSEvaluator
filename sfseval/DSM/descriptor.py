"""
author: Hang Zhou

class for handling the descriptor file for dataset
"""
import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from config import *
import json
import os

DESCRIPTOR_FILE_NAME="descriptor.json"

class DSDescriptor:
    json_field=["image","intrinsic","ground_truth","shape_prior","light"]
    ######################
    def __init__(self) -> None:
        self._meta={
            "size":1,
            "name":"new_dataset",
            "id":-1, # -1 means it's not registered
        }
        self.group=[dict()]
        self.group[0]["image"]={
            "img":None,
            "mask":None,
            "pose":None,
        }
        self.group[0]["intrinsic"]={
            "type":None,
            "path":None,
        }
        self.group[0]["ground_truth"]={
            "type":None,
            "path":None,
        }
        self.group[0]["shape_prior"]={
            "type":None,
            "path":None
        }
        self.group[0]["light"]=None

    def __from_json(self, ds_name) -> None:
        with open(DATASET_PATH+ds_name+"/"+DESCRIPTOR_FILE_NAME) as fp:
            jo=json.load(fp)
            self.group=[]
            for item in jo:
                new_obj=dict()
                for k in self.json_field:
                    new_obj[k]=item[k]
                self.group.append(new_obj)
            self._meta["name"]=ds_name
            self._meta["size"]=len(self.group)
    
    @classmethod
    def from_file(cls, ds_name):
        newObj=cls()
        try:
            newObj.__from_json(ds_name)
        except Exception as err:
            print("can't load descriptor file")
            raise
        else:
            return newObj

    # create descriptor for existing unstructured dataset
    @staticmethod
    def create_descriptor_file(name):
        newObj=DSDescriptor()
        newObj._meta["name"]=name
        mypath = DATASET_PATH+name
        if not os.path.isdir(mypath):
            print("No existing name folder found")
            return
        jo = json.dumps(newObj, indent=4,cls=DSDescriptorEncoder)
        with open(mypath+"/"+DESCRIPTOR_FILE_NAME, "w") as jfile:
            jfile.write(jo)   

    @staticmethod
    def create_new_dataset(name=None)->None:
        newObj=DSDescriptor()
        if name!=None:
            newObj._meta["name"]=name
        mypath = DATASET_PATH+newObj._meta["name"]
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        jo = json.dumps(newObj, indent=4,cls=DSDescriptorEncoder)
        with open(mypath+"/"+DESCRIPTOR_FILE_NAME, "w") as jfile:
            jfile.write(jo)
        
class DSDescriptorEncoder(json.JSONEncoder):
    def default(self, dobj:DSDescriptor):
        group=dobj.group
        json_field=dobj.json_field
        return group


if __name__ == "__main__":
    ds=DSDescriptor()
    ds.create_new_dataset()
    # ds=DSDescriptor()
    # ds.create_descriptor_file("figure-mvs")

    # ds=DSDescriptor.from_file("apple")

    # import pdb; pdb.set_trace()

