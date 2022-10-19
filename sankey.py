"""
Created on Sat Jul 23 10:17:58 2022
@author: Samsonite
"""
#%%
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
    lab = []
    for col in df:
        temp = df[col].unique()
        lab.append(temp)
    return lab
#%%
