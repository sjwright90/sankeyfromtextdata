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

#%%
