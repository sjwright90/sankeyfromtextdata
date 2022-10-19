"""
Created on Sat Jul 23 10:17:58 2022
@author: Samsonite
"""
#%%
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import itertools
import seaborn
#%%

grades = pd.read_excel("grades.xlsx")
#%%
def combinegrades(df, combine = ["AB", "DF"], group = ["A", "F"]):
    for c, g in zip(combine, group):
        df[df.isin(list(c))] = g
#%%
def countsdf(df):
    temp = df.value_counts(dropna = False)
    out = pd.DataFrame(temp)
    out.reset_index(inplace=True)
    out.rename(columns = {out.columns[-1]: "Count"}, inplace = True)
    return out
#%%
def rename(df):
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col] + "_" + col
#%%
def get_labels(df):
    lab = [df[col].unique() for col in df if col != "Count"]
    lab = list(itertools.chain.from_iterable(lab))
    lab = [v for v in lab if str(v).lower() != "nan"]
    return lab
#%%
def make_indexing(df, labels):
    df_c = df.copy()
    index_val = np.arange(len(labels))
    to_repl = dict(zip(labels, index_val))
    df_c.replace(to_repl, inplace = True)
    return df_c, to_repl
#%%
def get_source_target_value(df):
    source = []
    target = []
    value = []
    for col in df:
        temp = [int(i) for i in df[col] if str(i).lower() != "nan"]
        for i in range(len(temp) - 2):
            source.append(temp[i])
            target.append(temp[i+1])
            value.append(temp[-1])
    return source, target, value
#%%
fig = go.Figure(data=[go.Sankey(
    node = dict(
        label = labels
    ),
    link = dict(
        source = src,
        target = trg,
        value = val
    )
)])
fig.show()
#%%