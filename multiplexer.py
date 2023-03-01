"""

"""

import DSM
import RTM 
import CBM

# pseudo code
for algorithm in algorithms:
    for dataset in datasets:
        if check_if_runnable():
            results,error_msg = Run(algorithm, datasets, plugin)
            if error_msg:
                metrics=None
            else:
                metrics=cal_metric(result,dataset.groudtruth)
            save_metrics(metrics)



"""
$sfs run -a algo_id -d data_id

$sfs ds ls

$sfs ds up

$sfs ds compile

$sfs method ls

$sfs dsm 

$sfs cbm register

"""