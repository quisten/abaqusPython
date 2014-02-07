# python script to test sprind.py 

from sprind import sprind 
from odbAccess import * 
import sys 
import math 
import os 


# Get odb Name 
if len(sys.argv)>1: 
     odbName = sys.argv[1] 
else: 
     odbName = raw_input('Enter the name of the output database:').strip() 
if odbName.find('.odb')==-1: 
     odbName += '.odb' 


odb = openOdb(odbName) 

# Create the text file 
fileName = 'pValues.dat' 


if os.path.isfile(fileName): 
     fileName = raw_input('Enter the name of the text file: ').strip() 

outFile = open(fileName,'w') 

# Process all the frames of all the steps 
steps = odb.steps.values() 

ndiDict = {TENSOR_3D_FULL:3,TENSOR_3D_PLANAR:3,TENSOR_3D_SURFACE:2,TENSOR_2D_PLANAR:3,TENSOR_2D_SURFACE:2} 

varDict = {'S':'STRESS','E':'STRAINS'} 

#Loop through each step 
for step in steps: 
     stepName = step.name 
     #Loop through each frame 
     for frame in step.frames: 
         frameId = frame.frameId 
         outFile.write('**Step Name:\t'+stepName+'\tFrame Number:\t'+str(frameId)+'\n') 
         fo = frame.fieldOutputs 
         #Loop through stress and strain 
         for var in varDict.keys(): 
             if fo.has_key(var): 
                 varFO = fo[var] 
                 vals = varFO.values 
                 val0 = vals[0] 
                 ndi = ndiDict[varFO.type] 
                 nshr = len(val0.data)-ndi 
                 for val in vals: 
                     #Loop through each element and integration point 
                     line = '%s\tElement: %d\tIntegration Point: %d \n'%(varDict[var],val.elementLabel,val.integrationPoint) 
                     outFile.write(line) 
                     s = val.data 
                     ps,an = sprind(s,1,ndi,nshr) 
                     for i in range(3): 
                         line1 = 'PS%d   =%+1.8E'%(i+1,ps[i]) 
                         line2 = '\nPD%d1  =%+1.8E  PD%d2  =%+1.8E PD%d3  =%+1.8E\n\n'%(i+1,an[i][0],i+1,an[i][1],i+1,an[i][2]) 
                         outFile.write(line1+line2) 
outFile.close() 

print 'Successfully computed the principal values and directions.' 
print 'These principal values and directions are now available in %s' % (fileName) 

