"""
metrics object

should contains the 4d tabulate structure,
x: algorithm
y: dataset(dataset tags:object,light,camera prespective)
z: condition(hyper-params, shape_prior, initialization)
m: metrics
"""



"""
Table 1: X algorithm
-------------------------------------
dataset || MIT-apple   | MIT-Berkeley
tag     ||object-light | .......
-------------------------------------
    without priori
-------------------------------------
MAE     ||0.24987      | 0.8238       
MSE     || 0290458345  | 09045        
-------------------------------------
    with priori
-------------------------------------
MAE     ||0.24987      | 0.8238       
MSE     || 0290458345  | 09045       
-------------------------------------


Table 2: Y algorithm
-------------------------------------
dataset || MIT-apple   | MIT-Berkeley
tag     ||object-light | .......
-------------------------------------
    without priori
-------------------------------------
MAE     ||0.24987      | 0.8238       
MSE     || 0290458345  | 09045        
-------------------------------------
    with priori
-------------------------------------
MAE     ||0.24987      | 0.8238       
MSE     || 0290458345  | 09045       
-------------------------------------
"""