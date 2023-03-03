"""
author: Hang Zhou
"""

"""
codebase_obj: single executable/script api file, along with its configuration infomation,
                the api is expected to take: image etc, and takes optional input(light, albedo,shape,initialization)
dataset_obj: link to the dataset directory
"""
def RUN(codebase_obj, dataset_obj):
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
    # if mask missing
    dataset_obj

    if(code_type=="matlab"):
        import matlab.engine
        import matlab
        eng = matlab.engine.start_matlab()
        eng.cd(code_folder, nargout=0) # todo raw string

        # convert from file to matlab object
        # img=matlab.double([])
        img=eng.imread()
        mask=eng.imread()
        light=eng.load()
        intrinsic=eng.load()
        shape_prior=eng.load()
        output=eng.feval(code_api_name,img,mask,light,intrinsic,shape_prior)
        import pdb;pdb.set_trace()
        eng.quit()
    elif(code_type=="python"):
        return
    elif(code_type=="c"):
        return

    # calculate metric and save them!