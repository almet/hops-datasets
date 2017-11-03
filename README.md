# Hops data

This repository provides some tools to extract information from the websites of
hops merchants.

It scraps the websites and looks for information about hop oils and descriptions,
and then populates a *yaml* file with all the information it got.

Of course, the goal is to then re-use this information to transform it into
something easier to understand (but we're not there just yet!)

## Get the data

The extracted data is provided in the `*.yaml` files you see in the `data`
folder.

## Make it run

To make it run, simple run `make install` and the `make generate`. That should
work. You need to have python installed on your machine.

Enjoy!
