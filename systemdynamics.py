#system dynamics model
#example Lake level - Lake outflow system Lake Thun

import xlrd
import openpyxl
from scipy.interpolate import interp1d
import time
import pandas as pd

codespace="C:/DATA/develops/lakesystemdynamicsexample"
timesteps=range(0,73,1) #3 days
deltat=1 #hours
max(timesteps)
lakearea= 48300000
initial_lakelevel=583

inflow=pd.read_excel(codespace+"/"+"inputdata.xlsx", dtype="str", engine='openpyxl', sheet_name="inflow")
lakelevel=pd.read_excel(codespace+"/"+"inputdata.xlsx", dtype="str", engine='openpyxl', sheet_name="lakelevel")




