#!/usr/bin/python3

import re
import subprocess
import time
import os

with open('parameters.txt') as f:
    # get the names of the parameters we want to set
    # these are on the first line of the file parameters.txt
    names=[x for x in next(f).split()]
    print(names)
    # now read the parameter values in the following lines
    for i,line in enumerate(f):
        params=[x for x in line.split()]
        print(i,params)

        # check to see if the output directory for this run exists or
        # not
        output_dir='output'+str(i)
        if (os.path.isdir(output_dir)):
            print('Output directory %s exists!  Skipping...'%(output_dir))
        else:
            # replace the names in the template file with the values
            # from the parameter file, and save the result in parameters.py
            input_file=open('parameters_template.py','r')
            output_file=open('parameters.py','w')
            for line in input_file:
                newline=line
                for j,name in enumerate(names):
                    newline=re.sub('%'+name+'%',params[j],newline)
                output_file.write(newline)
            output_file.close()
            input_file.close()
            # now run the simulation code with that parameters.py
            output_file_for_this_run='output'+str(i)+'.out'
            subprocess_output=open(output_file_for_this_run,'w')
            subprocess.call(["./four-way_intersection.py"],stdout=subprocess_output)
            subprocess_output.close()
            # now copy any saved files to a safe place
            subprocess.call(["mkdir",'output'+str(i)])
            subprocess.call(["cp","four-way_intersection.mp4","road_stats.out","lt-vs-ct.png",'output'+str(i)+'.out','parameters.py','output'+str(i)])
