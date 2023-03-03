"""
author: Hang Zhou
"""

from CBM.cbm import MethodObj, CBM
from DSM.dsm import DatasetObj, DSM
"""
codebase_obj: single executable/script api file, along with its configuration infomation,
                the api is expected to take: image etc, and takes optional input(light, albedo,shape,initialization)
dataset_obj: link to the dataset directory
"""

def RUN(method_id=None, dataset_id=None, method_name=None, dataset_name=None):
    cbm=CBM()
    dsm=DSM()

    codebase_obj=cbm.get_by_name(method_name)
    dataset_obj=dsm.get_by_name(dataset_name)
    _run(codebase_obj,dataset_obj,0)

def _run(codebase_obj:MethodObj, dataset_obj:DatasetObj, stereo_idx:int):
    # input_dir <- dataset_obj.info
    # options = {
    # "shape_prior":1,
    # "light_prior":1,
    # "albedo_prior":0, #by default, optional
    # other optionals
    # ""
    # }
    # options are controled by user, or by config files, to FINE-CONTROL the algorithm behaviour, it's optional
    # hyper_params are controled by user, or by config files, to FINE-TUNE the algorithm, it's optional 


    # matlab
    # command = matlab -r "algorithm_api input_dir output_dir -with_shape_prior -with_light_prior -with_albedo_prior"
    # C
    # command = gcc 
    # twice ./myalgorithm input_dir output_dir is docker necessary this time?
    # docker_api.run(runtime_id, "command")

    # runtime obj is selected based on dataset_obj's information


    code_type=codebase_obj.get_type()
    code_folder=codebase_obj.get_folder()
    code_api_name=codebase_obj.get_api_name()

    # preprocess the dataset to complete all necessary field
    # get basic information
    # read image to get image dimension
    
    # if mask missing
    # import matlab.engine
    # import matlab
    # if dataset_obj.get_mask(stereo_idx)==None:
    #     mask=


    if(code_type=="matlab"):
        import matlab.engine
        import matlab
        import os
        code_api_name=os.path.splitext(code_api_name)[0]
        eng = matlab.engine.start_matlab()
        eng.cd(code_folder, nargout=0) # todo raw string
        # s = eng.genpath('myOuterFodler')
        # eng.addpath(s, nargout=0)

        # convert from file to matlab object
        # img=matlab.double([])
        # import pdb; pdb.set_trace()
        img=eng.imread(dataset_obj.get_image(stereo_idx))
        mask=eng.imread(dataset_obj.get_mask(stereo_idx))
        l_struct=eng.struct2cell(eng.load(dataset_obj.get_light(stereo_idx)))
        light=l_struct[0]
        # intrinsic=eng.load(dataset_obj.get_intrinsic(stereo_idx))
        # shape_prior=eng.load(dataset_obj.get_shape_prior(stereo_idx))
        intrinsic=eng.eye(3)
        shape_prior=eng.ones(eng.size(img,1),eng.size(img,2))
        # shape_prior=0
        # try:
        output=eng.feval(code_api_name,img,mask,light,intrinsic,shape_prior)
        # except:
        #     import pdb;pdb.set_trace()

        eng.quit()
    elif(code_type=="python"):
        return
    elif(code_type=="c"):
        return

    # calculate metric and save them!

RUN(method_name="variational_admm_sfs",dataset_name="apple")

