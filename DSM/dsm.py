"""
author: Hang Zhou

Dataset Management toolkit
"""
from pathlib import Path
import json
import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from config import *
from llist import dllist,dllistnode
from descriptor import DSDescriptor,DESCRIPTOR_FILE_NAME


"""
* start of dsm
dsm will start by reading the cached file(managed by framework), ignoring all unregisterd folder
If the cache file isn't correctly mapped to folders(some folder is missing), will update the cache file

* create new dataset
on creation, dataset should be empty, the folder is there, but it's not a valid dataset
after everything is done, should call register to formally add it to the management

* register a dataset
the correctness of dataset should be up to user
Once registered, name should never be modified

* get all dataset

"""

INDEX_FILE="./ds_index_file.json"

class DatasetObj:
    def __init__(self,name) -> None:
        self.name=name
        self.loaded=False
        # self.descriptor=DSDescriptor.from_file(name)

    def __eq__(self, other): 
        if not isinstance(other, DatasetObj):
            return NotImplemented
        return self.name == other.name
    
    def lazy_loading(func):
        def inner(*args):
            self=args[0]
            idx=args[1]
            if self.loaded:
                if idx>=self.size:
                    print("index out of bound for this dataset")
                    print("setting the default idx=0")
                    args[1]=0
                    return func(self,0)
                return func(*args)
            # first time load
            try:
                descriptor=DSDescriptor.from_file(self.name)
                self.group=descriptor.group
                self.size=descriptor._meta["size"]
            except Exception as err:
                print("dataset:"+self.name+" is not in legal structure")
                print("unregister this dataset")
                raise
            else:
                self.loaded=True
                if idx>=self.size:
                    print("index out of bound for this dataset")
                    print("setting the default idx=0")
                    return func(self,0)
                return func(*args)
        return inner

    @lazy_loading
    def get_image(self,idx)->str:
        return self.group[idx]["image"]["img"]
    
    @lazy_loading
    def get_mask(self,idx=0)->str:
        return self.group[idx]["image"]["mask"]
        
    @lazy_loading
    def get_pose(self,idx=0)->str:
        return self.group[idx]["image"]["pose"]

    @lazy_loading
    def get_intrinsic(self,idx=0):
        return self.group[idx]["intrinsic"]["path"],self.group[idx]["intrinsic"]["type"] 

    @lazy_loading
    def get_ground_truth(self,idx=0):
        return self.group[idx]["ground_truth"]["path"],self.group[idx]["ground_truth"]["type"]

    @lazy_loading
    def get_shape_prior(self,idx=0):
        return self.group[idx]["shape_prior"]["path"],self.group[idx]["shape_prior"]["type"]
 

    @lazy_loading
    def get_light(self,idx=0):
        return self.group[idx]["light"]


class DSM:
    __size=0
    __set=set()
    __lst=dllist() # llist of DatasetObj

    def __init__(self) -> None:
        cache_path=Path(INDEX_FILE)
        first=False
        if not cache_path.is_file():
            first=True
            cache_path.touch()
        self.__wakeup(first)
        print("dsm activated")

    def __wakeup(self,first):
        # scan through the folder and check if cache is intacted
        # if not, update cache
        # initialize all dataset objects
        if first: 
            return
        with open(INDEX_FILE,'r') as fp:
            try:
                jo=json.load(fp)
            except Exception:
                jo=None

       
        if jo==None:
            return
        self.__size=jo["size"]
        for name in jo["names"]:
            self.__lst.append(dllistnode(DatasetObj(name)))
            self.__set.add(name)
        # TODO check safety, but for now just ignore it

    def __push(self): # update cache file
        dict_obj={
            "size":self.__size,
            "names":list(self.__set),
        }
        jo=json.dumps(dict_obj)
        with open(INDEX_FILE, 'w') as fp:
            fp.write(jo)
    
    def __get(self,item:str):
        
        if item not in self.__set:
            return None
        the_node=DatasetObj(item)
        for i in range(0, self.__lst.size):
            # import pdb; pdb.set_trace()
            if self.__lst.nodeat(i).value==the_node:
                return the_node
        

    def __add(self,item:str):
        if item in self.__set:
            return
        self.__size+=1
        new_node = dllistnode(DatasetObj(item))
        self.__lst.append(new_node)
        self.__set.add(item)

    def __del(self,item:str):
        if item not in self.__set:
            return
        self.__size-=1
        new_node = DatasetObj(item)
        del self.__set[item]
        for i in range(0,self.__lst.size):
            target=self.__lst.nodeat(i).value
            if(new_node==target):
                self.__lst.remove(target)

    def reg(self, name): # only regist, but could break at runtime
        # check descriptor file is there
        thepath=Path(DATASET_PATH+name)
        thefile=Path(DATASET_PATH+name+"/"+DESCRIPTOR_FILE_NAME)
        if not thepath.exists():
            raise Exception("dataset folder doesn't exist")
        if not thefile.exists():
            raise Exception("descriptor file not found")
        self.__add(name)
        self.__push()

    def unreg(self,name):
        pass

    def ls(self):
        # only print name and id
        print("-------------------------------")
        print("id\t｜ name of datast\t|meta information")
        for i,node in enumerate(self.__lst):
            print(str(i+1)+"\t|"+node.name+"\t\t\t|")

    def get_all(self):
        all_obj=[]
        for lobj in self.__lst:
            all_obj.append(lobj)
        return all_obj
    
    def get_by_name(self,name)->DatasetObj: # id is just the index in the dataset
        # get name of id
        result = self.__get(name)
        if result==None:
            print("dataset name not exist")
        return result
        
    def get_by_id(self,id)->DatasetObj: # start from 1
        if id>self.__lst.size:
            print("dataset id not exist")
            return None
        
        return self.__lst.nodeat(id-1).value
    

if __name__=="__main__":
    dsm=DSM()
    dsm.reg("augustus-ps")
    dsm.reg("paper1")
    dsm.ls()
    r1=dsm.get_all()
    r2=dsm.get_by_name("augustus-ps")
    r3=dsm.get_by_id(1)
    # r3.get_image(1)
    import pdb; pdb.set_trace()
    r3
