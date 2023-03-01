"""
*OVERVIEW
this package provides methods to:
1. upload dataset
2. pull dataset
3. showing dataset

for uploading, it can only be accessed by cli
$ dsm reg - - -

for pulling, it can only be accessed by python api
$ rdataset.get()

for showing dataset, both cli and code are supported
$ rdataset.ls()
$ dsm ls

public api:
RData, RDataset
(DSM should be installed in server machine, local or remote)
dsm up(server side), register(client side), ls(cliend side), config(server side)

*DESCRIPTOR spec


*

"""