## 1. Overview
Here's slides for Shape from Shading algorithms introduction and the IO and design choice of evaluation process:
https://docs.google.com/presentation/d/1orHIz7jBYpMmg4C48Fh-Rspw64hOq1gSVDNbC3nZbG0/edit?usp=sharing

Our pipeline contains threes steps:
1. dataset registry
2. codebase registry
3. evaluation

First of all you need to download the dataset and code you try to evaluate.

You have to prepare the dataset by preprocessing the data into supported format(.mat file or image file). And you need to write a API file for the code s.t the tool could recognize the codebase and dataset.

The first two steps should be done manually. But in the end, you should register the them using the `sfs dsm --register` and `sfs cbm --register` commands provided by the tool.

Once you've register the legal dataset and codebase, you can view them and evaluating them using the `sfs run` command.

Each time you run the `run` command, If the codebase is bug-free, the evaluation result will be saved under `metrics_result` folder in the format of excel file combined with image filess. 

You can always add new dataset and codebase, just remember to register them.

## 2. Installation
### prerequisite
You need two things:
* A unix-based OS
* updated version of Matlab installed

Another thing strongly suggested:
* A Python>3.6 virtual environment

You can use anaconda/venv/virtualenv or similar tools, but here's a easy example, type them in the terminal:

1. `python3 -m venv venv`
2. `source ./venv/bin/activate`

Then you need to open the Matlab and type `matlabroot` in the console. Copy and paste the whole path, it might looks like this:
`'/Applications/MATLAB_R2022b.app'`

### install
Now run the script: `bash install.sh`

Notice it will prompt you for a path to Matlab root. Follow the guide of prompt

## 3. Dataset management
You need to preprocess the data into either image file or .mat file with your own effort.

And your next goal is to write a `descriptor.json` file inside a new dataset folder's root, providing all the important information about this dataset. Name your dataset properly, and move them into the `sfsevaluator/dataset` folder in this repository. A legal structure:
```
\sfsevaluator
    \sfseval
    \codebase
    \dataset
        \my_new_dataset_no_1
            - descriptor.json
            - other_data_files_in_this_dataset
        \my_new_dataset_no_2
            - descriptor.json
            - other_data_files_in_this_dataset
    - misc_files

```
After you're done with the json file and move it to the right location, next run this command:
```
sfs dsm --register your_new_dataset_name
```
Now you should be able to view all registered dataset with this command:
```
sfs dsm --list
```


### Descriptor file guide
Here's an example:
```
[
    {
        "image": {
            "img": "frame-000001.color.png",
            "mask": "frame-000001.mask.png",
            "pose": "frame-000001.pose.txt"
        },
        "intrinsic": {
            "type":"mat",
            "path":"colorIntrinsics.mat"
        },
        "ground_truth": {
            "type": null,
            "path": null
        },
        "shape_prior": {
            "type": "png",
            "path": "frame-000001.depth.png"
        },
        "light": null
    },
    {
        "image": {
            "img": "frame-000002.color.png",
            "mask": null,
            "pose": "frame-000002.pose.txt"
        },
        "intrinsic": {
            "type":"mat",
            "path":"colorIntrinsics.mat"
        },
        "ground_truth": {
            "type": null,
            "path": null
        },
        "shape_prior": {
            "type": "png",
            "path": "frame-000002.depth.png"
        },
        "light": null
    }
]
```
This is a dataset contains two images, each of the image is a [json object](
https://www.json.org/json-en.html#:~:text=An%20object%20is%20an%20unordered%20set%20of%20name/value%20pairs.%20An%20object%20begins%20with%20%7Bleft%20brace%20and%20ends%20with%20%7Dright%20brace.%20Each%20name%20is%20followed%20by%20%3Acolon%20and%20the%20name/value%20pairs%20are%20separated%20by%20%2Ccomma) in a [json array](https://www.json.org/json-en.html#:~:text=An%20array%20is%20an%20ordered%20collection%20of%20values.%20An%20array%20begins%20with%20%5Bleft%20bracket%20and%20ends%20with%20%5Dright%20bracket.%20Values%20are%20separated%20by%20%2Ccomma.). And the name-value pairs contains the information of each important data input for a SFS algorithm.

You can use this one as an example, but here's several rules for this file:
### WATCHOUT
1. if the dataset doesn't contains certain data, like ground truth data, that fields should be null. But write it like this:
```
"ground_truth": {
    "type": null,
    "path": null
}
```
DONNOT write it like this:
```
"ground_truth": null
```
AKA you still need to list all the fields, and mark each field as null.

2. The `path` field should contain a RELATIVE path to the data in your folder!

3. The `type` field only support two types of data: `mat` and image type `png`, `jpg`, `tiff` etc. But basically, if it's not `mat` type, it will be recognized as image type, so you can also write `img` in this field for an image.

4. The `light` component is by default, a `.mat` file, since it only should be a 9x3 or 9x1 vector(Not 3x9 1x9!). A use example:
```
"light":"L.mat"
```

5. The 'pose' field in `image` field is actually useless, don't expect it to do anything.

6. EACH `.mat` FILE SHOULD ONLY CONTAINS ONE VARIABLE! Don't squeeze multiple matlab variable into one `.mat` file, the tool will only read the FIRST variable in the `.mat` file! Remember this when you're preprocessing the dataset.

## 4. Codebase management
At this point, we only support algorithm writte in MATLAB!! But other languages could be supported with some effort.

Similar to database management, download the code, write an API file, move it to `/codebase` folder, and register it with:
`sfs cbm --register sfs_codebase_name`.

### API file guide(matlab)
```
function output = SFS_API(img, mask, light, intrinsic, shape_prior)
% img: a matrix of 3/1d, type double
% mask: a matrix of 1d, type double
% shape_prior: a matrix of 1d, type double, or NAN; optional
% intrinsic: a matrix of 3*3, type double
% light: a matrix of 9*1/9*3, type double, or NAN

% output is a structure with: depth, normal
```


### WATCHOUT
1. if a dataset doesn't provide camera intrisince data, the `intrinsic` argument of your api should expect a 3x3 identity matrix produced by the tool.
2. `output.depth` should be a 2d matrix!, `ouput.normal` should be a 3d matrix.
3. If you need to use different hyperparameters, modify it in your own API file!

## 5. Evaluation process
Once all done with the register, run the command
```
sfs run --ds_name your_dataset_name --cb_name your_codebase_name --tag your_tags_to_this_evluation
```
or you can run:
```
sfs run --ds_id your_dataset_id --cb_id your_codebase_id --tag your_tags_to_this_evluation
```
The id can be found by running `sfs cbm --list` and `sfs dsm --list` commands.
### Tags
The purpose of tag is to distinguish the evaluation with different hyperparameters. For example, you can run an algorithm with some virtual hyperparameter a=1. Next time you want to run it with a=2. You can use `--tag a_1` and `--tag a_2` for example.

## 6. Metrics
If the dataset doesn't provide ground truth data, of course no quantitative metrics can be calculated, only depth image and normal will be saved. Otherwise, two metrics will be calculated by default: MAE & RMSE.

Result will be saved in a tabular format(excel), and image data cell has a hyperlink to the image saved in correpsonding image folder.

## 7. Troubleshooting
When you run into trouble, you need to identify what's on this program's side and what's not. Typical user side errors:
1. The dataset is not correctly constructed.
2. The API for the algorithm is not bug free
3. The original code is not bug free, or this algorithm can't hanlde certain type of input data.

Most of the time bugs come from the wrong data format, the debug method is to add log or print information on your API file or their code to see what's wrong.

If you're certain that the bugs don't come from your side of work, here's the hack to debugging the our code:
In `sfseval/run.py` around line 81, add this line: `import pdb;pdb.set_trace()` and check it in pdb!

## 8. Modification
If you want to add more types of metric calculation, modify these places in `/sfseval/cal_metrics.py`:
1. Add your new field in `MetricDataObject: __init__` function
2. Add new field to END of `MetricsDB: heading` class variable(line 40)
3. Add two new line in `MetricsDB: get_metrics` function. And add a new function in this file for calculating your metrics (see what MAE did)