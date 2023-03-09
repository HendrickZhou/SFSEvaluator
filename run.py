"""
author: Hang Zhou
"""

from CBM.cbm import MethodObj, CBM
from DSM.dsm import DatasetObj, DSM
from util import create_dir
from cg_util import *
import matlab_agent
from cal_metric import cal_metrics
import os

"""
codebase_obj: single executable/script api file, along with its configuration infomation,
                the api is expected to take: image etc, and takes optional input(light, albedo,shape,initialization)
dataset_obj: link to the dataset directory
"""

RUNTIME_FOLDER_NAME="sfs_evaluator_runtime"
LOGGING_FILE_NAME="logging.log"

def RUN(method_id=None, dataset_id=None, method_name=None, dataset_name=None):
    cbm=CBM()
    dsm=DSM()

    codebase_obj=cbm.get_by_name(method_name)
    dataset_obj=dsm.get_by_name(dataset_name)
    _run(codebase_obj,dataset_obj,0)





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
def _run(codebase_obj:MethodObj, dataset_obj:DatasetObj, stereo_idx:int):
    code_type=codebase_obj.get_type()
    code_folder=codebase_obj.get_folder()
    code_api_name=codebase_obj.get_api_name()

    runtime_dir=create_dir(code_folder,RUNTIME_FOLDER_NAME)

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
        # import matlab.engine
        # import matlab
        code_api_name=os.path.splitext(code_api_name)[0]
        eng = get_eng()
        eng.cd(code_folder, nargout=0) # todo raw string

        # convert from file to matlab object
        img=eng.imread(dataset_obj.get_image(stereo_idx))
        mask=eng.imread(dataset_obj.get_mask(stereo_idx))
        l_struct=eng.struct2cell(eng.load(dataset_obj.get_light(stereo_idx)))
        light=l_struct[0]
        # intrinsic=eng.load(dataset_obj.get_intrinsic(stereo_idx))
        # shape_prior=eng.load(dataset_obj.get_shape_prior(stereo_idx))
        intrinsic=eng.eye(3)
        shape_prior=eng.ones(eng.size(img,1),eng.size(img,2))
        # shape_prior=0
        
        
        output=eng.feval(code_api_name,img,mask,light,intrinsic,shape_prior)
        
        # check correctness of output
        expected_fields=["depth","normal"]
        for field in expected_fields:
            if field not in output:
                print("output field missing, please check the API script for this codebase")
                return
        
        # convert output object to python native object
        # if field is not there, should set it to 0 or NaN
        depth=mat2np2d(output["depth"])
        mask=mat2np2d(mask)
        normal=None
        if output["normal"] is not None:
            normal=mat2np2d(output["normal"])
        # create output_obj
        tdobj=ThreeDObject()
        tdobj.from_data(depth=depth,mask=mask,normal=normal)
        import pdb;pdb.set_trace()
        eng.quit()

    elif(code_type=="python"):
        print("feature not supported yet")
        return
    elif(code_type=="c"):
        print("feature not supported yet")
        return

    # 3. calculate metric
    # get ground truth
    # if not ground truth, save the image
    if dataset_obj.get_ground_truth() is None:
        tdobj.vis_and_save()
    else:
        # if there's ground truth, calculate the metrics
        # ground truth is a standard depth image
        tdobj
        gt_type=dataset_obj.get_ground_truth_type()
        if gt_type is "mat":
            gt_data=imread(dataset_obj.get_ground_truth())
            gt_obj=ThreeDObject.from_data(depth=gt_data, mask=mask)
        else: # other 3d type including ply file
            gt_obj=ThreeDObject.from_file
        
        metrics=cal_metrics(tdobj, gt_obj)

    # 4. save metrics on database
    save_metrics(metrics)


if __name__=="__main__":
    RUN(method_name="variational_admm_sfs",dataset_name="apple")

