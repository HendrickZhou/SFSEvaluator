"""

"""


"""
codebase_obj: single executable/script api file, along with its configuration infomation,
                the api is expected to take: image etc, and takes optional input(light, albedo,shape,initialization)
dataset_obj: link to the dataset directory
"""
def RUN(codebase_obj, dataset_obj, options, hyper_params):
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
    docker_api.run(runtime_id, "command")

    # runtime obj is selected based on dataset_obj's information
    