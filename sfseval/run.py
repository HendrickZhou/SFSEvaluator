"""
author: Hang Zhou
"""

from CBM.cbm import MethodObj, CBM
from DSM.dsm import DatasetObj, DSM
from sfseval.util import *
from io_util import *
from cg_util import *
from cal_metric import get_metrics,vis_metrics,MetricsDB
import os

"""
codebase_obj: single executable/script api file, along with its configuration infomation,
                the api is expected to take: image etc, and takes optional input(light, albedo,shape,initialization)
dataset_obj: link to the dataset directory
"""

RUNTIME_FOLDER_NAME="sfs_evaluator_runtime"


def RUN(method_id=None, dataset_id=None, method_name=None, dataset_name=None, tags=[], stereo_idx: int=0):
    cbm=CBM()
    dsm=DSM()
    if method_id is None:
        codebase_obj=cbm.get_by_name(method_name)
    else:
        codebase_obj=cbm.get_by_id(method_id)

    if dataset_id is None:
        dataset_obj=dsm.get_by_name(dataset_name)
    else:
        dataset_obj=dsm.get_by_id(dataset_id)
    # process tags
    tag_set=set()
    for tag in tags:
        tag_set.add(tag)
    _run(codebase_obj,dataset_obj,stereo_idx,tag_set)

def _run(codebase_obj:MethodObj, dataset_obj:DatasetObj, stereo_idx:int,tag_set):
    """
    input_dir <- dataset_obj.info
    options = {
    "shape_prior":1,
    "light_prior":1,
    "albedo_prior":0, #by default, optional
    other optionals
    ""
    }
    options are controled by user, or by config files, to FINE-CONTROL the algorithm behaviour, it's optional
    hyper_params are controled by user, or by config files, to FINE-TUNE the algorithm, it's optional 
    """
    code_type=codebase_obj.get_type()
    code_folder=codebase_obj.get_folder()
    code_api_name=codebase_obj.get_api_name()

    # runtime_dir=create_dir(ondir=code_folder,name=RUNTIME_FOLDER_NAME)

    # 1. preprocess the dataset to complete all necessary field
    # including ground truth
    #
    # get basic information
    # read image to get image dimension
    
    # if mask missing
    # import matlab.engine
    # import matlab
    # if dataset_obj.get_mask(stereo_idx)==None:
    #     mask=

    tdobj=None

    # 2. run code
    if(code_type=="matlab"):
        code_api_name=os.path.splitext(code_api_name)[0]
        eng = get_eng()
        eng.cd(code_folder, nargout=0) # todo raw string

        # convert from file to matlab object
        try: 
            # TODO add type check!
            # import pdb;pdb.set_trace()
            img=get_image(dataset_obj.get_image(stereo_idx),FileType.IMG, DataType.MATLAB)
            mask=get_image(dataset_obj.get_mask(stereo_idx),FileType.IMG,DataType.MATLAB) # TODO maybe support mat?
            # TODO make sure mask is 1-d
            light=get_mat(dataset_obj.get_light(stereo_idx))
            intrinsic=get_mat(dataset_obj.get_intrinsic(stereo_idx))
            if intrinsic is None:
                intrinsic=eng.eye(3)
            shape_prior=get_image(dataset_obj.get_shape_prior(stereo_idx),
                                  dataset_obj.get_shape_prior_type(stereo_idx),
                                  DataType.MATLAB)
            # if size don't match
            if shape_prior is not None:
                iw=eng.size(img,1)
                ih=eng.size(img,2)
                sw=eng.size(shape_prior,1)
                sh=eng.size(shape_prior,2)
                if((iw,ih)!=(sw,sh)):
                    shape_prior=eng.imresize(shape_prior,matlab.double([iw,ih]))
            
        except Exception as e:
            breaker()
            print("dataset load failed")
            print("please check the dataset")
            breaker()
            return
        else:
            Print("Dataset loaded successfully")
            try:
                output=eng.feval(code_api_name,img,
                                 NANfy(mask),
                                 NANfy(light),
                                 NANfy(intrinsic),
                                 NANfy(shape_prior))
            except Exception as e:
                breaker()
                print("Exception occur during the execution")
                print("please check the API code!")
                breaker()
                return
            else:
                Print("SFS algorithm run successfully")

        # check correctness of output
        expected_fields=["depth","normal"]
        for field in expected_fields:
            if field not in output:
                Print("output field missing, please check the API script for this codebase")
                return
        
        # convert output object to python native object
        # if field is not there, should set it to 0 or NaN
        depth=mat2np2d(output["depth"])
        mask=mat2np2d(mask)
        normal=None
        if output["normal"] is not None:
            normal=mat2np3d(output["normal"])
        # create output_obj
        tdobj=ThreeDObject.from_data(depth=depth,mask=mask,normal=normal)
    elif(code_type=="python"):
        print("feature not supported yet")
        return
    elif(code_type=="c"):
        print("feature not supported yet")
        return

    # 3. calculate metric
    # visulise the result
    tdobj.show_depth()
    tdobj.show_normal()

    # get ground truth
    # if not ground truth, save the image
    m=None
    algorithm=codebase_obj.name
    dataset=dataset_obj.name
    if dataset_obj.get_ground_truth(stereo_idx) is None:
        m=vis_metrics(tdobj,
                      algorithm,
                      dataset,
                      tag_set
                      )
    else:
        # if there's ground truth, calculate the metrics
        # ground truth is a standard depth image
        gt_type=dataset_obj.get_ground_truth_type(stereo_idx)
        gt_path=dataset_obj.get_ground_truth(stereo_idx)
        img_np=None
        if gt_type == FileType.MAT:
            img_np=get_image(gt_path,FileType.MAT,DataType.NUMPY)
        elif gt_type == FileType.IMG:
            img_np=get_image(gt_path,FileType.IMG,DataType.NUMPY)
        else:
            raise WrongFormatError("unsupported ground truth data type")
        gt_obj = ThreeDObject.from_data(depth=img_np, mask=mask)
        # import pdb;pdb.set_trace()
        m=get_metrics(tdobj, gt_obj,algorithm,dataset,tag_set)

    # 4. save metrics on database
    with MetricsDB() as mdb:
        mdb.add_result(m)


if __name__=="__main__":
    # RUN(method_name="variational_admm_sfs",dataset_name="apple",tags=["natural light"])
    # RUN(method_name="SIRFS",dataset_name="apple",tags=["natural light"])
    # RUN(method_name="variational_admm_sfs", dataset_name="vase",tags=["light estimation"])
    # RUN(method_name="SIRFS", dataset_name="vase",tags=["light estimation"])
    # RUN(method_name="variational_admm_sfs",dataset_name="augustus-ps",tags=["light estimation"]) 
    # RUN(method_name="SIRFS", dataset_name="augustus-ps",tags=["light estimation"]) 
    RUN(method_name="variational_admm_sfs", dataset_name="figure-mvs",tags=["strong shape prior"]) 
    # RUN(method_name="SIRFS", dataset_name="figure-mvs",tags=["strong shape prior"]) 

