#system dynamics model
#example Lake level - Lake outflow system

import xlrd
import openpyxl
from scipy.interpolate import interp1d
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

codespace="C:/DATA/develops/lakesystemdynamicsexample"
timesteps=range(0,73,1) #3 days
deltat=1 #hours
max(timesteps)
addedvolume=0
lakearea= 48300000
#parameters to play with
initial_lakelevel=558
lakelevel=initial_lakelevel
initialoutflow=200.0
tunnelcapacity=100.0
securitylevel=400.0
timelag=24

#read the input data (non-linear relationships)
inflowdf=pd.read_excel(codespace+"/"+"inputdata.xlsx", dtype="float", engine='openpyxl', sheet_name="inflow")
lakeleveldf=pd.read_excel(codespace+"/"+"inputdata.xlsx", dtype="float", engine='openpyxl', sheet_name="lakelevel")

#plot the input data
plt.plot(inflowdf.hour, inflowdf.inflow)
plt.plot(lakeleveldf.lakelevel, lakeleveldf.increasevolume)
plt.plot(lakeleveldf.lakelevel, lakeleveldf.outflow)

#interpolation
x_vol=lakeleveldf.increasevolume.array
y_vol=lakeleveldf.lakelevel.array
f_lakelevel=interp1d(x_vol, y_vol, kind="linear")
#f_lakelevel(127454305)
x_outflow=lakeleveldf.lakelevel.array
y_outflow=lakeleveldf.outflow.array
f_outflow=interp1d(x_outflow, y_outflow, kind="linear")
#f_outflow(558.2)

#natural system without human intervention
lakelevellist=[initial_lakelevel]
outflowlist=[initialoutflow]
addedvolume=0
#iteration
for t in timesteps:
    print("timestep: " + str(t))
    if t>0:
        inflow=(inflowdf.loc[inflowdf["hour"]==t,"inflow"].values+inflowdf.loc[inflowdf["hour"]==t-1,"inflow"].values)/2.0
        inflow=inflow.tolist()[0]
        inflowvolume=inflow*deltat*3600
        addedvolume=addedvolume+inflowvolume
        lakelevel=f_lakelevel(addedvolume)
        outflow =float(f_outflow(lakelevel))
        outflowvolume=outflow*deltat*3600
        addedvolume=addedvolume-outflowvolume
        lakelevel = float(f_lakelevel(addedvolume))
        outflow = float(f_outflow(lakelevel))
        outflowlist.append(outflow)
        lakelevellist.append(float(f_lakelevel(addedvolume)))
        print("inflow: "+str(inflow))
        print("outflow: " + str(outflow))

#with human intervention - the relief tunnel: Tunnel adds surplus outflow of 100 m3/s if outflow < 400 m3/s
lakelevellist2=[initial_lakelevel]
outflowlist2=[initialoutflow]
addedvolume=0
#iteration
for t in timesteps:
    print("timestep: " + str(t))
    if t>0:
        inflow=inflowdf.loc[inflowdf["hour"]==t-1,"inflow"].values
        inflow = inflow.tolist()[0]
        inflowvolume=inflow*deltat*3600
        addedvolume=addedvolume+inflowvolume
        lakelevel=f_lakelevel(addedvolume)
        outflow =float(f_outflow(lakelevel))
        if outflow < securitylevel and outflow >150 and t > timelag:
            outflow=outflow+tunnelcapacity
        outflowvolume=outflow*deltat*3600
        addedvolume=addedvolume-outflowvolume
        lakelevel = float(f_lakelevel(addedvolume))
        outflow = float(f_outflow(lakelevel))
        if outflow < securitylevel and outflow >150:
            outflow=outflow+tunnelcapacity
        outflowlist2.append(outflow)
        lakelevellist2.append(f_lakelevel(addedvolume))


#System behavior if outflow exceeds a tipping point of 300 m3/s. 
#Above this outflow, discharge is increased by a factor of 1.5 due to lateral erosion
lakelevellist3=[initial_lakelevel]
outflowlist3=[initialoutflow]
addedvolume=0
#iteration
for t in timesteps:
    print("timestep: " + str(t))
    if t>0:
        inflow=inflowdf.loc[inflowdf["hour"]==t-1,"inflow"].values
        inflow = inflow.tolist()[0]
        inflowvolume=inflow*deltat*3600
        addedvolume=addedvolume+inflowvolume
        lakelevel=f_lakelevel(addedvolume)
        outflow =float(f_outflow(lakelevel))
        if outflow > 300:
            outflow=outflow*1.5
        outflowvolume=outflow*deltat*3600
        addedvolume=addedvolume-outflowvolume
        lakelevel = float(f_lakelevel(addedvolume))
        outflow = float(f_outflow(lakelevel))
        if outflow > 300:
            outflow=outflow*1.5
        outflowlist3.append(outflow)
        lakelevellist3.append(float(f_lakelevel(addedvolume)))



#Plot inflow-outflow and lake level
fig, axs = plt.subplots(1, 2, figsize=(9, 3), sharey=False)
fig.suptitle('lake level feedback')
axs[0].plot(inflowdf.hour, inflowdf.inflow, label="inflow")
axs[0].plot(inflowdf.hour.values.tolist(), outflowlist, label="outflow", color="blue")
axs[0].plot(inflowdf.hour.values.tolist(), outflowlist2, label="outflow with tunnel", color="red")
axs[0].plot(inflowdf.hour.values.tolist(), outflowlist3, label="outflow with erosion", color="green")
axs[0].legend(loc="best")
axs[0].set_xlabel("hour")
axs[0].set_ylabel("inflow/outflow [m3/s]")
axs[1].plot(inflowdf.hour.values.tolist(), lakelevellist, label="lake level", color="blue")
axs[1].plot(inflowdf.hour.values.tolist(), lakelevellist2, label="lake level with tunnel", color="red")
axs[1].plot(inflowdf.hour.values.tolist(), lakelevellist3, label="lake level with erosion", color="green")
axs[1].legend(loc="best")
axs[1].set_xlabel("hour")
axs[1].set_ylabel("lake level [m a.s.l.]")
plt.show()

