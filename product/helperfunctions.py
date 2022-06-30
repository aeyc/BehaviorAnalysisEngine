# -*- coding: utf-8 -*-
"""helperFunctions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18rMYExGP6aHMSVHValrZjXfb_7ll-T4v
"""

#%%
#LIBRARIES
#Data Processing
import pandas as pd
import numpy as np
import os, glob #To merge multiple csv files in given directory
import datetime

#Plots
import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib.pyplot import figure

#%%MERGE CSV
"""
mergeCSV function to merge csv files in the given directory
it creates a merged csv and saves it directly to the path where the code is running
"""
def mergeCSV(path):
    all_files = glob.glob(os.path.join(path, "events_*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
    df_merged   = pd.concat(df_from_each_file, ignore_index=True)
    df_merged.to_csv( "merged.csv")

#%%CREATE DICTIONARIES PER COLUMN
"""
uniqueValues function to find occurences of ther samples in the given df column
Takes dataframe column as list as an input
Outputs the sorted dictionary for occurences and the samples
"""
def uniqueValues(l):
  unique_dict = dict()
  for i in l:
    if i in unique_dict:
      unique_dict[i]+=1
    else:
      unique_dict[i]=1
  if not all(type(element)==int or float for element in list(unique_dict.values())):
    unique_dict =sorted(unique_dict.items(),key=operator.itemgetter(1),reverse=True)
  return unique_dict

#%%% SAVE DICTS
"""
saveDct method to save dictionaries 
which are created based on the number of occurences of the samples in a column
it takes the name of the file and dictionary as input parameters
creates a file with given name then saves it to the current directory which the code is executed
"""     
def saveDct(name, dct):   
    file = open("{}.txt".format(name),"w")
    for key, value in dct.items():
        file.write('%s:%s\n' % (key, value))
    file.close()

#%%PRINT DICTIONARIES PER COLUMN
"""

"""
def printDicts(df):
    unique_columns,nan_columns = [],[]
    for i in df.columns:
      print("-------COLUMN NAME: {}-------".format(i))
      if all(type(element)==float for element in list(df[i])) and np.isnan(list(df[i])).all():
        print("All values in the given column are NaN\n\n")
        nan_columns.append(i)
      else:
        dct = uniqueValues(df[i])
        saveDct(i,dct)
        if all(element == 1 for element in list(uniqueValues(df[i]).values())):
          print("All samples in the given column are unique")
          unique_columns.append(i)
        s = pd.Series(dct)
        print(s,"\n\n")

#%%DRAW PLOTS
"""
plot function to plot the graphs 
x and y are the names of the x,y axis labels of the plot respectively
plots and saves the plot

x: xaxis
y:yaxis
xl: data of x axis
yl:data of yaxis

isSaved: flag if the plot will be saved locally or not

fxsize: dimension of the figure (x axis)
fysize: dimension of the figure (y axis)
"""
def plot(x,y,xl,yl,style, isSaved,fxsize,fysize):
    plt.title("{} vs {}".format(x,y))
    plt.xlabel(x)
    plt.ylabel(y)
    if type(style)==int: 
        plt.plot(xl, yl, linewidth=style)
        desc = "line"
    else:
        plt.plot(xl, yl, style)
        desc = "dot"
    if isSaved:
        plt.rcParams['figure.figsize'] = [fxsize, fysize]
        plt.savefig('{}_{}_{}.png'.format(x,y,desc))
        
    plt.clf()
    plt.cla()
    plt.close()

"""# Handling Missing Values

s(t) presents the sample tracked at time t, whe s(t+$/tau$) presents the sample tracked $\tau$ later than the current t.

**Sample mean, estimate of correlation:** $\mathbf{c_s(\tau)} = \frac{1}{|V_\tau|} \sum_{t\in V_\tau} s(t) s(t+\tau)$

$\mathbf{V(\tau)}$ = { $t: s(t)$ $and$ $s(t+\tau)$ $are$ $both$ $avaiable$ }

**Variance of Confidence:** $\mathbf{\hat\sigma_{c_s(\tau)}} = \frac{1}{|V_\tau|^2} \sum_{t\in V_\tau} (s(t) s(t+\tau) - c_s(\tau))^2$

**Confidence Interval:** $(c_s(\tau) - 3\sigma_{c_s(\tau)}, c_s(\tau) + 3\sigma_{c_s(\tau)} )$
"""

#%%Fill the missing memory usage data woth previous or next day values
"""

"""
def fill_missing_previous(df):
  start_date = min(df["Timestamp"]).date()
  filled= []
  filled_tag = []
  for i in range(len(df)):
    if np.isnan(df.iloc[i]["Memoria Usata"]):
      if df.iloc[i]["Timestamp"].date()!= start_date:
        df.iloc[i]["Memoria Usata"] = df[df.Timestamp ==df["Timestamp"].iloc[i]-datetime.timedelta(days=1)]["Memoria Usata"].values[0]
        df.at[i,"Memoria Usata"]= df[df.Timestamp ==df["Timestamp"].iloc[i]-datetime.timedelta(days=1)]["Memoria Usata"].values[0]
        filled.append( df[df.Timestamp ==df["Timestamp"].iloc[i]-datetime.timedelta(days=1)]["Memoria Usata"].values[0])
        filled_tag.append("previous")
      else:
        j = df["Timestamp"].iloc[i]+datetime.timedelta(days=1)
        while np.isnan(df[df.Timestamp ==j]["Memoria Usata"].values[0]):
          j += datetime.timedelta(days=1)
          
        filled.append(df[df.Timestamp ==j]["Memoria Usata"].values[0])
        df.at[i,"Memoria Usata"] = df[df.Timestamp ==j]["Memoria Usata"].values[0]
        filled_tag.append("next")
    else:
      filled.append(df.iloc[i]["Memoria Usata"])
      filled_tag.append("current")
  return filled, filled_tag