# cmplot.py - Cloudy Mountain Plot in python

An informative RDI categorical distribution plot inspired by Violin, Bean and Pirate Plots.

(RDI = Raw data + Descriptive statistics + Inferential statistics)

* Like [Violin plots](https://en.wikipedia.org/wiki/Violin_plot), it shows smoothed kernel density curves, revealing information which would be hidden in boxplots, for example presence of multiple *"peaks"* ("modes") in the distribution *"mountain"*.

* Like [Bean plots](https://www.jstatsoft.org/article/view/v028c01), it shows the raw data, drawn as a *cloud* of points. By default all data points are shown but you can optionally control this and limit the display to a subset of the data.

* Like [Pirate plots](https://github.com/ndphillips/yarrr), it marks confidence intervals (either from Student's T or as Bayesian Highest Density Intervals or as interquantile ranges) for the probable position of the true population mean.

Since by default it does not symmetrically mirror the density curves, it allows immediate comparisions of distributions side-by-side.

## Download and installation

`cmplot` is pure python code. It has no platform-specific dependencies and should thus work on all platforms. It requires the packages `plotly numpy scipy pandas`. The latest version of `cmplot` can be installed by typing either:

``` bash
> pip3 install cmplot
```
  ([Python Package Index](https://pypi.org/project/cmplot/))

or:
```
> pip3 install git+git://github.com/g-insana/cmplot.py.git
```
  ([GitHub](https://github.com/g-insana/cmplot.py/).

There is also a [version in Julia](https://github.com/g-insana/CMPlot.jl/).

## Documentation

Check the online documentation and jupyter notebook for usage and examples at the [GitHub page](https://github.com/g-insana/cmplot.py/).

## Quickstart

``` python
>>> import plotly.graph_objects as go
>>> from cmplot import cmplot

 #call the cmplot directly inside a plotly Figure function as:

>>> go.Figure(*cmplot(mydataframe,xcol="xsymbol"))

 #alternatively get traces and layout as separate variables, so that you can modify them or combine with others before passing them to Figure() function:

>>> (traces,layout)=(cmplot(mydataframe,xcol="xsymbol"))

 #[...] do something with traces/layout

>>> go.Figure(traces,layout) #plot it
```

## Copyright

`cmplot` is licensed under the [GNU Affero General Public License](https://choosealicense.com/licenses/agpl-3.0/).

(c) Copyright [Giuseppe Insana](http://insana.net), 2019-
