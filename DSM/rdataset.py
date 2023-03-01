'''
Author: Hang Zhou

reconstruction dataset definition

'''
from typing import Any
from client import get_data

'''
Serialized object
'''
class _SObj():
    def __init__(self) -> None:
        pass


class ReconData:
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def get(self, id: str):
        pass

    def serialize(self):
        pass

    def deserialize(self):
        pass


class ReconDataset:
    def __init__(self) -> None:
        pass

    def __next__(self):
        pass

    ####
    # IO
    ####
    def _register(self, path: str, name: str, descriptor: str):
        # _compile_dataset
        # _serialized
        pass

    @staticmethod
    def get(id):
        data=ReconDataset()
        sobj=get_data()
        data._deserialize()
        return data
        
    ####
    # Helper
    ####
    # build complete rdataset obj from descriptor function
    def _compile_dataset(self, path, name, descriptor):
        # read descriptor and build
        pass


    def _serialize(self):
        pass

    def _deserialize(self):
        pass