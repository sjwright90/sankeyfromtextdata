"""
Created on Sat Jul 23 10:17:58 2022
@author: Samsonite
"""
#%%
'''This file contains a series of functions used to transform and manipulate a csv or xlsx file into
a format appropriate for drawing a Sankey diagram and then producing said sankey diagram.
The tabular data does already need to be in a specific format. Each column should represent 
one event (in this case a given class offered in a given year). Each row will be an individual 
path through said events (in this case the grades a student got in a given class). Each cell 
contains the given result of the individual and that event (for example a "B" in "Calc1_2020"). 
The functions were built assuming string data would be the input, but I think numerical data 
would work. The intent of this work was to make a Sankey plot to track how students flowed 
through a series of college courses, the data set provided as an example is just randomly 
generated data, but shows how the process works. I believe the code should be highly adaptable 
to any instance where one is trying to make a sankey plot of categorical data, again some 
formating of your data set might be needed before it will work though.'''
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import itertools
from seaborn import color_palette as sns_pal
#%%

def make_clr_tup(palete = "Set1", alpha = 0.5):
    '''Takes a color set from seaborn (default is "Set3" from colorbrewer) and 
    transforms it into a list of strings in the form: "rgba(1,1,1,1)"
    Args:
        palete: string object of a named color palete available in seaborn
        alpha: float 0.0-1.0, the alpha level to set for all colors
    Returns:
        List of strings in the form "rgba(x,x,x,alpha)
    '''
    clrpl = [list(c) + [alpha] for c in sns_pal(palete)]
    clrpl = ["rgba" + str(tuple(c)) for c in clrpl]
    return clrpl
#%%
grades = pd.read_excel("grades.xlsx")
#%%
def combinegrades(df, combine = ["AB", "DF"], group = ["A", "F"]):
    '''Groups fields in data frame based on input.
    Args:
        combine: list of strings to be combined. Strings to be grouped written all as one
            string (ie "AB" will be "A" and "B").
        group: list of strings to replace strings identified by the combine, needs to be same length
            as combine
    '''
    for c, g in zip(combine, group):
        df[df.isin(list(c))] = g
#%%
def countsdf(df):
    '''Applies value_counts to entire data frame, then converts results into a new data frame, 
    and renames final column to "Count". Gives count of each unique path through data frame.
    Args:
        df: a pandas data frame
    Returns:
        pandas data frame'''
    temp = df.value_counts(dropna = False)
    out = pd.DataFrame(temp)
    out.reset_index(inplace=True)
    out.rename(columns = {out.columns[-1]: "Count"}, inplace = True)
    return out
#%%
def rename(df):
    '''Renames each item in data frame by adding the column name to all the strings in that column
    Args:
        df: a pandas dataframe
    '''
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col] + "_" + col
#%%
def get_labels(df):
    '''Gets all unique string values in the data frame.
    Args:
        df: a pandas dataframe
    Returns:
        list: list of strings of all unique string values in the data frame'''
    lab = [df[col].unique() for col in df if col != "Count"]
    lab = list(itertools.chain.from_iterable(lab))
    lab = [v for v in lab if str(v).lower() != "nan"]
    return lab
#%%
def make_indexing(df, labels):
    '''Replaces all unique labels in a data frame with an integer value corresponding to that 
    label's index location in a list of the unique labels.
    Args:
        df: pandas data frame
        labels: list of all unique strings in the data frame
    Returns:
        df_c: copy of the data frame with the strings recoded as numerical (presence of nan will cause int to 
            automatically be converted to floats)
        to_repl: a dictionary mapping strings to replacement values'''
    df_c = df.copy()
    index_val = np.arange(len(labels))
    to_repl = dict(zip(labels, index_val))
    df_c.replace(to_repl, inplace = True)
    return df_c, to_repl
#%%
def get_source_target_value(df, color = False, colorset = None, alpha = 0.5):
    '''Creates three lists of integers for input into Sankey plotter
    Args:
        df: a pandas data frame consisting only of int and np.nan
        color: bool, default False. Use True if you want to get 
            a color list for the links, by default will give 
            one color for each unique first node
        colorset: default None, by default will use colorbrewer Set1 palete, 
            replace with appropriate string of palete from Seaborn library
            to change from default palete
        alpha: float default 0.5, alpha value for the links colors
    Returns:
        source: list of int corresponding to points in a Sankey diagram that
            have links coming out of them
        target: list of int corresponding to points in a Sankey diagram that
            have links coming into them
        value: thickness of a links connecting source and target
        '''
    if color:
        if isinstance(colorset, str):
            if alpha >= 0 and alpha <= 1:
                clrs = make_clr_tup(palete=colorset, alpha=alpha)
            else: 
                clrs = make_clr_tup(palete = colorset)
        else: clrs = make_clr_tup()
        plotclrs = []
    source = []
    target = []
    value = []
    for col in df:
        temp = [int(i) for i in df[col] if str(i).lower() != "nan"]
        if color: tempclr = clrs[temp[0]]
        for i in range(len(temp) - 2):
            source.append(temp[i])
            target.append(temp[i+1])
            value.append(temp[-1])
            if color: plotclrs.append(tempclr)
    if color:
            return source, target, value, plotclrs
    return source, target, value
#%%
def node_colors(labels, plotcolors, alpha = None):
    '''Creates a list to color the nodes by, based on labels and current
    colors allocated to the links, all other nodes will be grey
    Args:
        labels: list of labels that will be used in the Sankey diagram
        plotcolors: colors already generated to color the links in the diagram
        alpha: default None, change to float between 0-1 to change default
            0.5 for alpha value of node color'''
    
    node_color = list(dict.fromkeys(plotcolors))
    if alpha and alpha<=1 and alpha >=0:
        alpha = str(alpha) + ")"
        node_color = [color.replace("0.5)", alpha) for color in node_color]
    base = "rgba(0.5,0.5,0.5,0.3)"
    while len(node_color) < len(labels):
        node_color.append(base)
   
    return node_color

#%%
def plot_sankeyd(labels,src, trg, val, save = False, plotcolors = None, nodecolors = None):
    '''Plots a Sankey diagram.
    Args:
        labels: list of strings, labels for each node in Sankey
        src: source nodes
        trg: target nodes
        val: thickness of link connecting source nodes and target nodes
        save: bool, default False, use True if you want to export the file to html.
            If True will prompt for file path
        plotcolors: default None, if given list of rgba color strings 
            will color links using the list
        nodecolors: default None, if given list of rgba color strings
            will color nodes accordingly, see node_colors() function for
            making the list
        '''
    labels = [item.replace("_", " ") for item in labels]
    nodesdict = dict(label = labels)
    if nodecolors: nodesdict["color"] = nodecolors
    linksdict = dict(
                source = src,
                target = trg,
                value = val 
                )
    if plotcolors: linksdict["color"] = plotcolors
    fig = go.Figure(data=[go.Sankey(
        node = nodesdict,
            link = linksdict)])
    fig.show()
    if save:
        location = input("Path and file name to save as (if saving in local folder just use filename):")
        fig.write_html(location + ".html")
#%%