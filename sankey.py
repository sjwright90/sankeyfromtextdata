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
def make_clr_tup(palette = "Set1", alpha = 0.5):
    '''Transforms Seaborn color palette into appropriate format for plotly plotting
    
    Parameters:
    ----------
    palette : string
        A seaborn color palette
            
    alpha: float {0.0-1.0}
        The alpha level to set for all colors
    
    
    Returns:
    ----------
    clrpl :
        List of strings in the form "rgba(x,x,x,alpha)"
    '''
    
    
    clrpl = [list(c) + [alpha] for c in sns_pal(palette)]
    clrpl = ["rgba" + str(tuple(c)) for c in clrpl]
    return clrpl


def combinegrades(df, combine = ["AB", "DF"], group = ["A", "F"]):
    '''Rename categorical features in data frame by grouping. 
    
    Parameters:
    ----------
    
    combine : list of strings
        Strings to be grouped written all as one string (eg "AB" will be "A" and "B").
        
    group : list of strings
        strings to replace with, needs to be same length as combine
    '''
    
    
    for c, g in zip(combine, group):
        df[df.isin(list(c))] = g


def countsdf(df):
    '''Get each unique path through the data frame and number of each pathway
    
    Applies value_counts to entire data frame, then converts results into a new data frame, 
    and renames final column to "Count". Gives count of each unique path through data frame. 
    
    Parameters:
    ----------
    
    df : pandas dataframe
    
    
    Returns :
    ----------
    
    out : pandas dataframe'''
    
    
    temp = df.value_counts(dropna = False)
    out = pd.DataFrame(temp)
    out.reset_index(inplace=True)
    out.rename(columns = {out.columns[-1]: "Count"}, inplace = True)
    return out


def rename(df):
    '''Renames each item in data frame using column names. 
    
    Parameters:
    ----------
    
    df: pandas dataframe
    
    '''
    
    
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col] + "_" + col

            
def get_labels(df):
    '''Gets all unique string values in the data frame. 
    
    Parameters:
    ----------
    
    df : pandas dataframe
    
    
    Returns:
    ----------
    
    list : list of strings
    
    '''
    
    
    lab = [df[col].unique() for col in df if col != "Count"]
    lab = list(itertools.chain.from_iterable(lab))
    lab = [v for v in lab if str(v).lower() != "nan"]
    return lab


def make_indexing(df, labels):
    '''Replaces all unique labels in a data frame with an integer value corresponding to that 
    label's index location in a list of the unique labels. 
    
    Parameters:
    ----------
    
    df : pandas data frame
    
    labels : list of strings
    
        list of all unique strings in the dataframe
    
    
    Returns:
    ----------
    
    df_c : pandas data frame
    
        copy of the data frame with the strings replaced with numerical or np.NaN
            
    to_repl : dict
        a dictionary mapping strings to replacement values
    
    '''
    
    
    df_c = df.copy()
    index_val = np.arange(len(labels))
    to_repl = dict(zip(labels, index_val))
    df_c.replace(to_repl, inplace = True)
    return df_c, to_repl


def get_source_target_value(df, color = False, colorset = None, alpha = 0.5):
    '''Creates three lists of integers for input into Sankey plotter 
    
    Parameters:
    ----------
    
    df : a pandas data frame consisting only of int and np.nan
    
    color : bool, default False. Use True if you want to get 
            a color list for the links, by default will give 
            one color for each unique first node
            
    colorset : default None, by default will use colorbrewer Set1 palete, 
            replace with appropriate string of palete from Seaborn library
            to change from default palete
    alpha : float default 0.5, alpha value for the links colors
    
    
    Returns:
    ----------
    
    source: list
        list of int corresponding to nodes in a Sankey diagram that
            have links coming out of them
            
    target : list
    
        list of integers corresponding to nodes in a Sankey diagram that
        have links feeding into them
        
    value : list
    
        thickness of a links connecting source and target
        
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

def node_colors(labels, plotcolors, alpha = None):
    '''Creates a list to color the nodes by, based on labels and current
    colors allocated to the links, all other nodes will be grey. 
    
    Parameters:
    ----------
        
    labels : list-like
    
        list of labels that will be used in the Sankey diagram
        
    plotcolors : list-like
    
        colors already generated to color the links in the diagram
        
    alpha : default None
    
        change to float between 0-1 to define alpha of node color, default alpha is 0.5
        
    '''
    
    
    node_color = list(dict.fromkeys(plotcolors))
    
    if alpha and alpha<=1 and alpha >=0:
        alpha = str(alpha) + ")"
        node_color = [color.replace("0.5)", alpha) for color in node_color]
        
    base = "rgba(0.5,0.5,0.5,0.3)"
    
    while len(node_color) < len(labels):
        node_color.append(base)
   
    return node_color


def plot_sankeyd(labels,src, trg, val, save = False, plotcolors = None, nodecolors = None, show_fig = False):
    '''Plots a Sankey diagram. 
    
    Parameters:
    ----------
    
    labels : list-like
        List of strings, labels for each node in Sankey
    
    src : list-like
        List of integers, source nodes
    
    trg : list-like
        List of integers, target nodes
    
    val : list-like
        List of integers, thickness of link connecting source nodes and target nodes
        
    save : bool 
        Default False, use True if to export the plot to html. If True will prompt for file path.
    
    plotcolors : list-like
        Default None, if given list of colors will color links using the list
        
    nodecolors : list-like
        Default None, if given list of colors will color nodes accordingly
            
    show_fig : bool
        Default False, use True to display the figure
    
    Returns:
    ----------
    
    fig : plotly object
        Returned if "save" set to True
        
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
    if show_fig: 
        fig.show()

    if save:
        location = input("Path and file name to save as (if saving in local folder just use filename):")
        fig.write_html(location + ".html")
    
    return fig
