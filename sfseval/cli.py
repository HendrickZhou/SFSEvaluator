"""command line entry
@Author: Hang Zhou
"""
import argparse
from sfseval.DSM.dsm import DSM
from sfseval.CBM.cbm import CBM
from sfseval.run import RUN

# sfs
parser = argparse.ArgumentParser(prog="sfs",
                                add_help=True,
                                usage="sfs [-h] {dsm,cbm,run}")
subparser = parser.add_subparsers(required=True)

# sfs dsm
parser_dsm = subparser.add_parser("dsm",
                        description="dataset management",
                        add_help=True,
                        aliases="dataset")
parser_dsm.set_defaults(which="dsm")
group_dsm = parser_dsm.add_mutually_exclusive_group(required=True)
group_dsm.add_argument("--list", "-ls",
                    dest="ls",
                    help="list all registered dataset",
                    action="store_true")
group_dsm.add_argument("--register", "-reg",
                    help="register the dataset given name",
                    metavar="dataset_name",
                    dest="ds_name")

# sfs cbm
parser_cbm = subparser.add_parser("cbm",
                        description="codebase management",
                        add_help=True,
                        aliases="codebase")
parser_cbm.set_defaults(which="cbm")
group_cbm = parser_cbm.add_mutually_exclusive_group(required=True)
group_cbm.add_argument("--list", "-ls",
                        dest="ls",
                        help="list all registered codebase",
                        action="store_true")
group_cbm.add_argument("--register", "-reg",
                        help="register the codebase given name",
                        dest="cb_name")

# sfs run --ds_id xxx --cb_name yyy --tags
# if name is the same with id(aka a number), recognize it as id! So don't name it as pure number
parser_run = subparser.add_parser("run",
                        description="run the evaluation given dataset and codebase",
                        add_help=True)
parser_run.set_defaults(which="run")
group_run_dataset = parser_run.add_mutually_exclusive_group(required=True)
group_run_dataset.add_argument("--ds_id","-di",
                        dest="ds_id",
                        type=int,
                        help="dataset id")
group_run_dataset.add_argument("--ds_name","-dn",
                        dest="ds_name",
                        help="dataset name")

group_run_codebase = parser_run.add_mutually_exclusive_group(required=True)
group_run_codebase.add_argument("--cb_id","-ci",
                        dest="cb_id",
                        type=int,
                        help="codebase id")
group_run_codebase.add_argument("--cb_name","-cn",
                        dest="cb_name",
                        help="codebase name")
parser_run.add_argument("--tags",
                        nargs='*',
                        help="tags of this run")

def main():
    global parser
    final_args = parser.parse_args()
    if final_args.which == 'dsm':
        dsm=DSM()
        if final_args.ls:
            dsm.ls()
        else:
            try:
                dsm.reg(final_args.ds_name)
            except Exception as e:
                print("can't register the dataset!")
                print("Please check if the new dataset folder name is correct!")
            finally:
                print("Closing dsm")
    elif final_args.which == 'cbm':
        cbm=CBM()
        if final_args.ls:
            cbm.ls()
        else:
            try:
                cbm.reg(final_args.cb_name)
            except Exception as e:
                print("can't register the codebase!")
                print("Please check if the new codebase folder name is correct!")
            finally:
                print("Closing cbm")
    else: # run
        method_id = dataset_id = method_name = dataset_name = None
        if final_args.ds_id is None:
            dataset_name = final_args.ds_name
        else:
            dataset_id = final_args.ds_id

        if final_args.cb_id is None:
            method_name = final_args.cb_name
        else:
            method_id = final_args.cb_id
        RUN(method_id=method_id, dataset_id=dataset_id, method_name=method_name, dataset_name=dataset_name,tags=final_args.tags)
    
if __name__ == "__main__":
    main()