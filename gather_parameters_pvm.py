#!/usr/bin/python3

import matplotlib.pyplot as plt
import re
import subprocess
import time
import os
from math import *

name='pvm'
f=open('parameters.txt')
# get the names of the parameters we want to set
# these are on the first line of the file parameters.txt
names=[x for x in next(f).split()]
index=[i for i,p in enumerate(names) if p==name][0]
print(index)
vlist=[]
allist=[]
nlist=[]
al2list=[]
# now read the parameter values in the following lines
for i,line in enumerate(f):
    params=[x for x in line.split()]
    
    # check to see if the output directory for this run exists or
    # not
    output_dir='output'+str(i)
    if (os.path.isdir(output_dir)):
        print('Output directory %s exists!  Reading...'%(output_dir))
        g=open('%s/road_stats.out'%(output_dir))
        names=[x for x in next(g).split()]
        sumlifetime=0
        sumlifetime2=0
        n=0
        for dataline in g:
            data=dataline.split()
            j=int(data[0])
            creationtime=float(data[1])
            deletiontime=float(data[2])
            lifetime=float(data[3])
            sumlifetime+=lifetime
            sumlifetime2+=lifetime**2
            n+=1
        avglifetime=sumlifetime/n
        avglifetime2=sumlifetime2/n
        print(params,avglifetime)
        vlist.append(int(params[index]))
        allist.append(avglifetime)
        nlist.append(n)
        al2list.append(avglifetime2)
        g.close()
f.close()
plt.scatter(vlist,allist)
plt.xlabel('Average Velocity (m/s)')
plt.ylabel('Average Lifetime of Car (s)')
print(vlist,allist,nlist,al2list)
unique_vlist=[]
for item in vlist:
    if item not in unique_vlist:
        unique_vlist.append(item)
print(unique_vlist)
unique_allist=[]
unique_al2list=[]
unique_stdev=[]
for v in unique_vlist:
    suml=0
    sumn=0
    suml2=0
    for i,testv in enumerate(vlist):
        if v==testv:
            suml+=allist[i]*nlist[i]
            sumn+=nlist[i]
            suml2+=al2list[i]*nlist[i]
    al=suml/sumn
    al2=suml2/sumn
    stdev=sqrt(al2-al**2)*sqrt(1/(sumn-1)) # actually standard error of mean
    unique_allist.append(al)
    unique_al2list.append(al2)
    unique_stdev.append(stdev)
print(unique_allist,unique_al2list,unique_stdev)

plt.errorbar(unique_vlist,unique_allist,yerr=unique_stdev,fmt="o",color='red')
plt.show()
