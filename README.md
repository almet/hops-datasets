# Hops datasets

This repository aims to provide datasets about hop varieties..

It has been extracted from the websites of hops merchants and then enhanced by
hand.

Some information might not be correct, since the sources are sparse.

If you want to give me a hand on this (propose changes, new sources, update the data) don't hesitate to open an issue, a pull-request, or to contact me at
`alexis - at - notmyidea - dot - org`. Thanks.

## Visualisations

Here are some data-visualisation created from this dataset:

### Hop oils concentration breakout

[![/viz/oils/hops-oils-breakout.png?raw=true](/viz/oils/hops-oils-breakout.png?raw=true)](https://almet.github.io/hops-datasets/viz/oils/)

### How hop varieties relate to each other?

[![/viz/lineage/lineage.png?raw=true](/viz/lineage/lineage.png?raw=true)](https://almet.github.io/hops-datasets/viz/lineage/)

## Data units

When not specified, here are the units used:

- Total Oils in *ml/100g*
- Cohumulone in *percentage of the alpha acids*
- Caryophyllene in *percentage of total oils*
- Farnesene in *percentage of total oils*
- Geraniol in *percentage of total oils*
- Humulene in *percentage of total oils*
- Myrcene in *percentage of total oils*

## Sources

- http://simplyhops.fr/hops/hop-pellets
- https://ychhops.com/varieties

Parenthood information has been taken from:

- http://beervana.blogspot.fr/2012/09/hop-varieties-reference-guide.html
- The description of the varieties themselves


## Want to run the scrappers yourself?

The scrappers have proven useful to generate the first version of the dataset,
but since the data has been enhanced manually since, are quite useless to me.

Nevertheless, if you want to make them run, simply run `make install` to
install the dependencies and then `make generate`.

You need to have python installed on your machine. After these commands have completed, you should have the datasets generated locally. Enjoy!
