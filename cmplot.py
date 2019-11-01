"""
    cmplot is OpenSource Python code to plot and compare
    categorical data using Cloudy Mountain plots

    Copyright (C) 2019- Giuseppe Insana

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact the developer: <http://insana.net/i/#contact>
    Online documentation: <https://cmplot.readthedocs.io>
"""

from random import shuffle, randint
from scipy.stats import t
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def cmplot(data_frame: pd.core.frame.DataFrame, xcol=None, ycol=None,
           xsuperimposed=False, xlabel=None, ylabel=None, title=None,
           orientation="h", inf="hdi", conf_level=0.95, hdi_iter=10000,
           showboxplot=True, ycolorgroups=True, side="alt",
           altsidesflip=False, spanmode=None, showpoints=True,
           pointsoverdens=False, pointsopacity=0.4, markoutliers=True,
           colorrange=None, colorshift=0, pointshapes=None,
           pointsdistance=0.6, pointsmaxdisplayed=0):
    """
    Cloudy Mountain Plot:
        an RDI (Raw data, Descriptive statistics, and Inferential data)
        categorical distribution plot inspired by Violin, Bean and Pirate plots

    Coded in Julia & Python by Dr Giuseppe Insana, Aug & Oct 2019

    Online documentation: <https://cmplot.readthedocs.io>

    Arguments:
        The only mandatory arguments for CMPlot are a dataframe containing the
        data and either a string or a list of strings which label the columns
        containing the discrete independent variables in the dataframe, as shown
        above in the Quickstart section.

        Several additional optional arguments can be specified to customize the
        result, both in terms of content and of form.

        * `xcol`: a string or an array of strings, column name(s) of the
        dataframe that you wish to plot as "x".

        This should be the categorical independent variable. If more than one
        column name is given, the combination of these will be used as "x". See
        examples for interpretation. e.g. `xcol="Species"`

        * `ycol`: a string or an array of strings, column name(s) of the
        dataframe that you wish to plot as "y". Optional.

        These should be the continuous dependent variables. If ycol is not
        specified, then the function will plot all the columns of the dataframe
        except those specified in `xcol`.

        e.g. `ycol=["Sepal.Length","Sepal.Width"]` would plot sepals' length and
        width as a function of the flower species

        * `orientation`: 'h' | 'v', default is 'h'

        Orientation of the plot (horizontal or vertical)

        * `xsuperimposed`: boolean, default is False

        The default behaviour is to plot each value of the categorical variable
        (or each combination of values for multiple categorical variables) in a
        separate position. Set to True to superimpose the plots. This is useful
        in combination with "side='alt'" to create asymmetrical plots and
        comparing combinations of categorical variables (e.g. Married + Gender ~
        Wage).

        * `xlabel`: string or list of strings

        Override for labelling (and placing) the plots of the categorical
        variables. Only relevant when using `xsuperimposed`

        * `ylabel`: string or list of strings

        Override for labelling the dependent variables. If not specified,
        the labels for the dataframe ycol are used.

        * `title`: string

        If not specified, the plot title will be automatically created from the
        names of the variables plotted.

        e.g. `title="Length of petals for the three species"`

        * `side`: 'pos' | 'neg' | 'both' | 'alt', default is 'alt'

        'pos' would create kernel density curves rising towards the positive end
        of the axis, 'neg' towards the negative, 'both' creates symmetric curves
        (like violin/bean/pirate plots). 'alt' will alternate between 'pos' and
        'neg' in case where multiple ycol are plotted.

        e.g. `side='both'`

        * altsidesflip: boolean, default is False

        Set to True to flip the order of alternation between sides for the
        kernel density curves. Only relevant when `side`='alt'

        * `ycolorgroups`: boolean, default is True

        Set to False to have the function assign a separate colour when plotting
        different values of the categorical variable. Leave as True if all
        should be coloured the same.

        * `spanmode`: 'soft' | 'hard', default is 'soft'

        Controls the rounding of the kernel density curves or their sharp drop at
        their extremities. With 'hard' the span goes from the sample's minimum to
        its maximum value and no further.

        * `pointsoverdens`: boolean, default is False

        Set to True to plot the raw data points over the kernel density curves.
        This is obviously the case when `side`='both', but otherwise by default
        points are plotted on the opposite side.

        * `showpoints`: boolean, default is True

        Set to False to avoid plotting the cloud of data points

        * `pointsopacity`: float, range 0-1, default is 0.4

        The default is to plot the data points at 40% opacity. 1 would make
        points completely opaque and 0 completely transparent (in that case
        you'd be better served by setting `showpoints` to False).

        * `inf`: 'hdi' | 'ci' | 'iqr' | 'none', default is 'hdi'

        To select the method to use for calculating the confidence interval for
        the inference band around the mean. 'hdi' for Bayesian Highest Density
        Interval, 'ci' for Confidence Interval based on Student's T, 'iqr' for
        Inter Quantile Range. Use 'none' to avoid plotting the inference band.

        * conf_level: float, range 0-1, default is 0.95

        Confidence level to use when `inf`='ci', credible mass for `inf`='hdi'

        * hdi_iter: integer, default is 10000

        Iterations to use when performing Bayesian t-test when `inf`='hdi'

        * showboxplot: boolean, default is True

        Set to False to avoid displaying the mini boxplot

        * markoutliers: boolean, default is True

        Set to False to avoid marking the outliers

        * pointshapes: array of strings

        You can specify manually which symbols to use for each distribution
        plotted. If not specified, a random symbol is chosen for each
        distribution.

        * pointsdistance: float, range 0-1, default is 0.6

        Distance at which data points will be plotted, measured from the base of
        the density curve. 0 is at the base, 1 is at the top.

        * pointsmaxdisplayed: integer, default is 0

        This option sets the maximum number of points to be drawn on the graph.
        The default value '0' corresponds to no limit (plot all points). This
        option can be useful when the data amount is massive and would prove
        inefficient or inelegant to plot.

        * colorrange: integer, default is None

        By default, the distribution will be coloured independently, with the
        colours automatically chosen as needed for a single plot, maximising the
        difference in hue across the colour spectrum. You can override this by
        specifying a number to accomodate. This is useful when joining different
        plots together. E.g. if the total number of colours to be accomodating,
        after joining two plots, would equal 4, then set colorrange=4

        * colorshift: integer, default is 0

        This option is used in combination with `colorrange` to skip a certain
        amount of colours when they are to be assigned to the distributions to
        be plotted. This is useful when joining different plots together, to
        avoid having distributions plotted with the same colour.

    Returns:
        * traces: list of instances of plotly.graph_objs.Violin
        * layout: instance of plotly.graph_objs.Layout
    """

    # # 0) Helper functions:
    def t_test_ci(x_val, conf_level=0.95):
        """
        t_test confidence interval: T-distribution based confidence interval when
            population variance is unknown
        note: the t-confidence interval hinges on the normality assumption
            of the data
        """
        deg_freedom = len(x_val) - 1
        return t.interval(conf_level, deg_freedom, loc=np.mean(x_val),
                          scale=np.std(x_val) / np.sqrt(len(x_val)))

    def hdi_from_mcmc(posterior_samples, credible_mass=0.95):
        """
        Computes highest density interval from a sample of representative values,
        estimated as the shortest credible interval
        Takes Arguments posterior_samples (samples from posterior) and credible
        mass (normally .95)
        Originally from https://stackoverflow.com/questions/22284502/
             highest-posterior-density-region-and-central-credible-region
        Arguments:
            posterior_samples=array of values
            credible_mass (default 0.95)
        Returns: low and hi range for the HDI
        """
        sorted_points = sorted(posterior_samples)
        ci_idx_inc = np.ceil(credible_mass * len(sorted_points)).astype('int')
        n_ci = len(sorted_points) - ci_idx_inc
        ci_width = [0] * n_ci
        for i in range(0, n_ci):
            ci_width[i] = sorted_points[i + ci_idx_inc] - sorted_points[i]
        hdi_min = sorted_points[ci_width.index(min(ci_width))]
        hdi_max = sorted_points[ci_width.index(min(ci_width)) + ci_idx_inc]
        return hdi_min, hdi_max

    def ttest_bayes_ci(x_val, iterations=1000, credible_mass=0.95):
        """
        Originally from https://github.com/tszanalytics/BayesTesting.jl
        Adapted and extended by Giuseppe Insana on 2019.08.19
        Arguments:
            x_val=array of values
            iterations=iterations for samples of posterior
            credible_mass (for HDI highest density interval)
        Returns:
            hdi: highest density interval of posterior for specified credible_mass
        """
        num = len(x_val)
        dof = num - 1
        xmean = np.mean(x_val)
        std_err = np.std(x_val) / np.sqrt(num)
        t_s = std_err * t.rvs(dof, size=iterations) + xmean
        hdi = hdi_from_mcmc(t_s, credible_mass=credible_mass)
        return hdi

    # # 1) Arguments' parsing:

    dfsymbols = data_frame.columns #all column names

    if xcol is None:
        raise TypeError("you need to specify xcol argument, e.g. 'Species'")

    xsymbols = []
    if isinstance(xcol, list):
        xsymbols = xcol #already array of symbols
    else:
        xsymbols = [xcol] #create array of a single symbol

    #check sanity of specified xcol(s)
    if len(set(xsymbols).intersection(set(dfsymbols))) != len(set(xsymbols)):
        raise ValueError("xcol contains symbols not present in the dataframe")

    ysymbols = []
    if ycol is None:
        ysymbols = list(set(dfsymbols).difference(set(xsymbols)))
    else:
        if isinstance(ycol, list): #if specified
            ysymbols = ycol #already an array of symbols
        else:
            ysymbols = [ycol] #create array of a single symbol

        #check sanity of specified ycols
        if len(set(ysymbols).intersection(set(dfsymbols))) != len(set(ysymbols)):
            raise ValueError("ycol contains symbols not present in the dataframe")

        if set(xsymbols).intersection(set(ysymbols)): #check for common symbols
            raise ValueError("ycol and xcol should not contain the same symbol(s)!")

    if orientation not in ('v', 'h'):
        raise ValueError("if defining orientation, use either h or v")

    if inf not in ('hdi', 'ci', 'iqr', 'none'):
        raise ValueError("if defining inference band type, use either \
                ci (Student's t-test confidence intervals) \
                or hdi (Bayesian Posterior Highest Density Interval) \
                or iqr (InterQuartileRange) \
                or none (no band)")

    plot_title = ""
    if title is None:
        plot_title = ', '.join(xsymbols) + ' ~ ' + ', '.join(ysymbols)
    else:
        plot_title = title

    if xlabel is not None:
        if not isinstance(xlabel, list): #if it's not already an array, make it so
            xlabel = [xlabel]

    if ylabel is not None:
        if not isinstance(ylabel, list): #if it's not already an array, make it so
            ylabel = [ylabel]
        if len(ysymbols) != len(ylabel):
            print("WARNING: you specified ", len(ylabel),
                  " ylabel overrides but you are plotting ", len(ysymbols),
                  " dependent variables => labels will be cycled")

    if spanmode is None:
        spanmode = 'soft'
    else:
        if spanmode not in ('soft', 'hard'):
            raise ValueError("if defining spanmode, only 'soft' and 'hard' are allowed values")

    # # 2) divide up data by xsymbols and then ysymbol and calculate stats, preparing datas array:

    datas = []
    sides_x = {} #useful when xsuperimposed
    sideindex = 0
    xlabelsoverride = {} #useful when xsuperimposed
    xlabelindex = 0
    ylabelindex = 0
    rand_int = randint(1, 10000)

    #separating distributions for each categorical x:
    for label, sub_data_frame in data_frame.groupby(xsymbols):
        for ysymbol in ysymbols: #by default for all Ys present (or all those specified)
            xvalue = label if not isinstance(label, tuple) else "&".join([str(x) for x in label])
            xname = "&".join(xsymbols)
            if ylabel is None:
                yname = ysymbol
            else:
                yname = ylabel[ylabelindex % len(ylabel)]
                ylabelindex += 1
                print("NOTE: ylabel {} -> {}".format(ysymbol, yname))
            #x = ["&".join(r) for r in sub_data_frame[xsymbols].values]
            y_val = sub_data_frame[ysymbol].values
            if len(y_val) < 2: #cannot compute inf
                y_lo, y_hi = (None, None)
            else:
                y_lo, y_hi = ttest_bayes_ci(y_val, iterations=hdi_iter,
                                            credible_mass=conf_level) if inf == "hdi" \
                    else t_test_ci(y_val, conf_level=conf_level) if inf == "ci" \
                    else np.quantile(y_val, [0.25, 0.75]) if inf == "iqr" \
                    else (None, None)
            #print("confidence: {} .. {}".format(y_lo, y_hi))
            #y_mode = maximum(modes(y_val))
            if xsuperimposed:
                thislabel = str(sub_data_frame[xsymbols].iloc[0][0])
                if xlabel is None:
                    x_0 = " " if len(xsymbols) == 1 else thislabel
                else:
                    if thislabel not in xlabelsoverride:
                        xlabelsoverride[thislabel] = xlabel[xlabelindex % len(xlabel)]
                        xlabelindex += 1
                        print("NOTE: xlabel {} -> {}".format(thislabel, xlabelsoverride[thislabel]))
                    x_0 = xlabelsoverride[thislabel]
                if len(xsymbols) == 1:
                    x_1 = xvalue
                else:
                    x_1 = str(sub_data_frame[xsymbols].iloc[0][-1])
            else:
                x_0 = xvalue
                x_1 = xvalue

            if x_1 not in sides_x:
                sideindex += 1
                sides_x[x_1] = sideindex

            data = {
                'xvalue': str(xvalue),
                'xname': xname,
                'yname': yname,
                'x_0': x_0,
                'x_1': x_1,
                'y_val': y_val,
                #mode=y_mode,
                'lo': y_lo,
                'hi': y_hi
            }
            datas.append(data)

    # # 3.1) Stylistic variants:
    sides = []
    jitter = 0.3
    if side == "both":
        sides = ["both"]
        jitter = 0.4
        pointpositions = [0]
    elif side == "alt":
        if altsidesflip:
            sides = ["positive", "negative"]
            pointpositions = [-pointsdistance, pointsdistance]
        else:
            sides = ["negative", "positive"]
            pointpositions = [pointsdistance, -pointsdistance]
    elif side == "pos":
        sides = ["positive"]
        pointpositions = [-pointsdistance]
    elif side == "neg":
        sides = ["negative"]
        pointpositions = [pointsdistance]
    else:
        raise ValueError("if defining side, use one of both|alt|pos|neg")

    if pointsoverdens:
        #invert the values and hence the sides of the raw points positions
        pointpositions = [-x for x in pointpositions]
        #(not applicable when side==both)

    label_seen = {}
    if ycolorgroups:
        legend_tracegroupgap = 0
    else:
        legend_tracegroupgap = 10

    # # 3.2) Coloring setup
    colorarraylength = len(datas)
    colorindexes = {}

    if ycolorgroups:
        i = colorshift #override 0 index start if colorshift specified
        for data in datas:
            if data['yname'] not in colorindexes:
                i += 1
                colorindexes[data['yname']] = i
        colorarraylength = len(colorindexes)

    if colorrange is not None: #then override colorarraylength
        colorarraylength = colorrange

    colorstart = 0
    colorend = 330
    if colorarraylength > 12:
        colorend = 350

    colorstep = colorend // colorarraylength #integer division
    fillcolors = ["hsla({}, 50%, 50%, 0.3)".format(j) for j in
                  range(colorstart, colorend + 1, colorstep)]
    linecolors = ["hsla({}, 20%, 20%, 0.8)".format(j) for j in
                  range(colorstart, colorend + 1, colorstep)]
    markerlinecolors = ["hsla({}, 20%, 20%, 0.4)".format(j) for j in
                        range(colorstart, colorend + 1, colorstep)]
    markerfillcolors = ["hsla({}, 70%, 70%, 1)".format(j) for j in
                        range(colorstart, colorend + 1, colorstep)]
    if pointshapes is not None: #override given
        if isinstance(pointshapes, list):
            markersymbols = pointshapes
        else:
            raise TypeError("pointshapes must be an Array of markersymbol strings, \
                    e.g. [\"circle\", \"diamond\"]")
    else:
        markersymbols = ["circle", "diamond", "cross", "triangle-up",
                         "triangle-left", "triangle-right",
                         "triangle-down", "pentagon", "hexagon", "star",
                         "hexagram", "star-triangle-up",
                         "star-square", "star-diamond"]
        shuffle(markersymbols) #change randomly symbols at each call of the function

    cifillcolors = ["hsla({}, 45%, 45%, 0.4)".format(j) for j in
                    range(colorstart, colorend + 1, colorstep)]
    boxlinecolors = ["hsla({}, 30%, 30%, 1)".format(j) for j in
                     range(colorstart, colorend + 1, colorstep)]
    outliercolors = ["hsla({}, 50%, 50%, 0.9)".format(j) for j in
                     range(colorstart, colorend + 1, colorstep)]

    # # 4) Define traces:

    traces = []
    i = colorshift #override 0 index start if colorshift specified
    for data in datas:
        if ycolorgroups:
            i = colorindexes[data['yname']]
            label = data['yname']
            legendgroup = data['yname']
            legend_tracegroupgap = 0
        else:
            i += 1 #if no ycoloring, then simply choose a new color
            label = str(data['yname'] + " " + data['xvalue'])
            legendgroup = data['xvalue']
            legend_tracegroupgap = 10

        showlegend = True
        if label in label_seen:
            showlegend = False #stop adding new legends if already printed one
        else:
            label_seen[label] = True

        traces.append(
            go.Violin( # main trace: kernel density + raw data + meanline
                orientation=orientation,
                x0=data['x_0'] if orientation == "v" else None,
                x=None if orientation == "v" else data['y_val'],
                y0=None if orientation == "v" else data['x_0'],
                y=data['y_val'] if orientation == "v" else None,
                width=0,
                name=label,
                showlegend=showlegend,
                points="all" if showpoints and (pointsmaxdisplayed == 0 or \
                                                pointsmaxdisplayed >= len(data['y_val'])) \
                             else False,
                jitter=jitter,
                pointpos=pointpositions[sides_x[data['x_1']] % len(pointpositions)] \
                         if xsuperimposed \
                         else pointpositions[i % len(pointpositions)],
                spanmode=spanmode,
                scalemode="count",
                scalegroup=data['xvalue'] + str(rand_int),
                legendgroup=legendgroup,
                line={'width': 1, 'color': linecolors[i % len(linecolors)]},
                side=sides[sides_x[data['x_1']] % len(sides)] \
                     if xsuperimposed else sides[i % len(sides)],
                #text="mode: ".format(data['mode']),
                hoveron="points+kde+violins",
                hoverinfo="y+name+text" if orientation == "v" else "x+name+text",
                hoverlabel={'bgcolor': cifillcolors[i % len(cifillcolors)]},
                meanline={'visible': True, 'width': 1, 'color': linecolors[i % len(linecolors)]},
                fillcolor=fillcolors[i % len(fillcolors)],
                marker={'opacity': pointsopacity, 'size': 9, \
                        'color': markerfillcolors[i % len(markerfillcolors)], \
                        'line': {'width': 0.5, \
                                 'color': markerlinecolors[i % len(markerlinecolors)]}, \
                        'symbol': markersymbols[i % len(markersymbols)]}
            ) #violin
        ) #append
        if showpoints and pointsmaxdisplayed != 0 and pointsmaxdisplayed < len(data['y_val']):
            #if only a reduced number of points needs to be displayed
            traces.append(
                go.Violin( #optional trace: points by themselves
                    orientation=orientation,
                    x0=data['x_0'] if orientation == "v" else None,
                    x=None if orientation == "v" else data['y_val'][0:pointsmaxdisplayed],
                    y0=None if orientation == "v" else data['x_0'],
                    y=data['y_val'][0:pointsmaxdisplayed] if orientation == "v" else None,
                    width=0,
                    name="",
                    showlegend=False,
                    scalegroup=data['xvalue'] + str(rand_int),
                    legendgroup=legendgroup,
                    #hoverinfo="none",
                    points="all",
                    hoveron="points",
                    hoverinfo="y" if orientation == "v" else "x",
                    jitter=jitter,
                    pointpos=pointpositions[sides_x[data['x_1']] % len(pointpositions)] \
                             if xsuperimposed \
                             else pointpositions[i % len(pointpositions)],
                    meanline_visible=False,
                    box_visible=False,
                    spanmode=spanmode,
                    fillcolor="rgba(0, 0, 0, 0)",
                    line={'width': 0, 'color': "rgba(0, 0, 0, 0)"},
                    side=sides[sides_x[data['x_1']] % len(sides)] \
                         if xsuperimposed else sides[i % len(sides)],
                    marker={'opacity': pointsopacity, 'size': 9, \
                            'color': markerfillcolors[i % len(markerfillcolors)], \
                            'line': {'width': 0.5,
                                     'color': markerlinecolors[i % len(markerlinecolors)]}, \
                            'symbol': markersymbols[i % len(markersymbols)] \
                            }
                ) #optional trace for reduced number of points
            ) #push
        #end if pointsmaxdisplayed != 0
        if data['lo'] is not None:
            traces.append(
                go.Violin( #secondary trace: interval band
                    orientation=orientation,
                    x0=data['x_0'] if orientation == "v" else None,
                    x=None if orientation == "v" else data['y_val'],
                    y0=None if orientation == "v" else data['x_0'],
                    y=data['y_val'] if orientation == "v" else None,
                    width=0,
                    #name=data.yname,
                    name="",
                    showlegend=False,
                    #scalemode="count",
                    scalegroup=data['xvalue'] + str(rand_int),
                    legendgroup=legendgroup,
                    hoverinfo="none",
                    points="outliers" if markoutliers else False,
                    jitter=0,
                    pointpos=0,
                    meanline_visible=False,
                    box_visible=showboxplot,
                    box={'fillcolor': "rgba(0, 0, 0, 0)", 'width': 0.25, \
                         'line_color': boxlinecolors[i % len(boxlinecolors)], 'line_width': 0.5},
                    spanmode="manual",
                    span=(data['lo'], data['hi']),
                    line_width=0,
                    fillcolor=cifillcolors[i % len(cifillcolors)],
                    side=sides[sides_x[data['x_1']] % len(sides)] \
                         if xsuperimposed else sides[i % len(sides)],
                    marker={'size': 11, #OUTLIERS ONLY
                            'symbol': markersymbols[i % len(markersymbols)], \
                            'color': outliercolors[i % len(outliercolors)], \
                            'line': {'width': 0.5,
                                     'color': markerlinecolors[i % len(markerlinecolors)]}}
                ) #second violin trace for interval band
            ) #push
        #end if data.lo is not None
    #end for data in datas

    # # 5) Define layout
    layout = go.Layout(
        paper_bgcolor="#eeeeff",
        plot_bgcolor="#ffffff",
        showlegend=True,
        legend_tracegroupgap=legend_tracegroupgap,
        violingap=0, violingroupgap=0,
        violinmode="overlay",
        yaxis_side="left",
        title=plot_title,
        title_x=0.5,
        margin={'l': 80, 'r': 10, 't': 10, 'b': 40},
        legend={'x': 1.1, 'y': 1.1, 'xanchor': "right"},
        xaxis={
            'showline': True, 'showticklabels': True,
            'zeroline': True, 'visible': True, 'showgrid': orientation == "v"
        },
        yaxis={
            'showline': True, 'showticklabels': True,
            'zeroline': True, 'visible': True, 'showgrid': orientation == "h"
        },
        xaxis_title=str(', '.join(ysymbols)) if orientation == "h"
        else str(', '.join(xsymbols)),
        yaxis_title=str(', '.join(xsymbols)) if orientation == "h"
        else str(', '.join(ysymbols)),
    )

    # # 6) return both traces and layout, so that layout can be further tweaked
    # #      (or traces added) before plotting
    return traces, layout
