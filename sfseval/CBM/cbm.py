""" Method Management toolkit
@author: Hang Zhou
"""

from pathlib import Path
import json
from sfseval.config import *
from llist import dllist,dllistnode

INDEX_FILE="method_index_file.json"
METHOD_DESCRIPTOR_FILE="API.json"

class MethodDescriptor:
    def __init__(self) -> None:
        self.type=None
        self.api=None
        self._meta=dict()

    @classmethod
    def from_file(cls,method_name):
        newObj=cls()
        try:
            newObj.__from_json(method_name)
        except Exception as err:
            print("can't load descriptor file")
            raise
        else:
            return newObj

    def __from_json(self, method_name):
        with open(METHOD_PATH+method_name+"/"+METHOD_DESCRIPTOR_FILE) as fp:
            jo=json.load(fp)
            self.type=jo["type"]
            self.api=jo["api"]
            self._meta["name"]=method_name

class MethodObj:
    def __init__(self,name) -> None:
        self.name=name
        self.__load(name)

    def __eq__(self, other): 
        if not isinstance(other, MethodObj):
            return NotImplemented
        return self.name == other.name
    
    def __load(self,name):
        obj=MethodDescriptor.from_file(name)
        self.type=obj.type
        self.api=obj.api

    def get_type(self):
        return self.type

    def get_folder(self):
        return METHOD_PATH+self.name+"/"

    def get_api_name(self):
        return self.api


class CBM:
    __size=0
    __set=set()
    __lst=dllist() # llist of DatasetObj

    def __init__(self) -> None:
        lib_path=Path(__file__).parent.resolve()
        cache_path=Path.joinpath(lib_path, INDEX_FILE)
        first=False
        if not cache_path.is_file():
            first=True
            cache_path.touch()
        self.cache_path=cache_path
        self.__wakeup(first)
        print("cbm activated")

    def __wakeup(self,first):
        """
        scan through the folder and check if cache is intacted
        if not, update cache
        initialize all dataset objects
        """
        if first: 
            return
        with open(self.cache_path,'r') as fp:
            try:
                jo=json.load(fp)
            except Exception:
                jo=None

       
        if jo==None:
            return
        self.__size=jo["size"]
        for name in jo["names"]:
            self.__lst.append(dllistnode(MethodObj(name)))
            self.__set.add(name)
        # TODO check safety, but for now just ignore it

    def __push(self): # update cache file
        dict_obj={
            "size":self.__size,
            "names":list(self.__set),
        }
        jo=json.dumps(dict_obj)
        with open(self.cache_path, 'w') as fp:
            fp.write(jo)
    
    def __get(self,item:str):
        
        if item not in self.__set:
            return None
        the_node=MethodObj(item)
        for i in range(0, self.__lst.size):
            # import pdb; pdb.set_trace()
            if self.__lst.nodeat(i).value==the_node:
                return the_node
        

    def __add(self,item:str):
        if item in self.__set:
            return
        self.__size+=1
        new_node = dllistnode(MethodObj(item)) 
        self.__lst.append(new_node)
        self.__set.add(item)

    # def __del(self,item:str):
    #     if item not in self.__set:
    #         return
    #     self.__size-=1
    #     new_node = DatasetObj(item)
    #     del self.__set[item]
    #     for i in range(0,self.__lst.size):
    #         target=self.__lst.nodeat(i).value
    #         if(new_node==target):
    #             self.__lst.remove(target)

    def reg(self, name): # only regist, but could break at runtime
        # check descriptor file is there
        thepath=Path(METHOD_PATH+name)
        thefile=Path(METHOD_PATH+name+"/"+METHOD_DESCRIPTOR_FILE)
        if not thepath.exists():
            raise Exception("method folder doesn't exist")
        if not thefile.exists():
            raise Exception("descriptor file not found")
        self.__add(name)
        self.__push()

    def ls(self):
        # only print name and id
        print("-------------------------------")
        print("id\t｜ name of method\t|meta information")
        for i,node in enumerate(self.__lst):
            print(str(i+1)+"\t|"+node.name+"\t\t\t|")

    def get_all(self):
        all_obj=[]
        for lobj in self.__lst:
            all_obj.append(lobj)
        return all_obj
    
    def get_by_name(self,name):
        # get name of id
        result = self.__get(name)
        if result==None:
            print("method name not exist")
        return result
        
    def get_by_id(self,id): 
        # start from 1
        if id>self.__lst.size:
            print("method id not exist")
            return None
        
        return self.__lst.nodeat(id-1).value
    

if __name__=="__main__":
    cbm=CBM()
    cbm.reg("SIRFS")
    cbm.reg("variational_admm_sfs")
    cbm.ls()
    r1=cbm.get_all()
    r2=cbm.get_by_name("SIRFS")
    r3=cbm.get_by_id(1)
    # r3.get_image(1)
    import pdb; pdb.set_trace()
    r3