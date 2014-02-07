#Made by J.T.B. Overvelde on 9 may 2011

#execute job
mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
    SINGLE, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=
    modelName2, modelPrint=OFF, multiprocessingMode=DEFAULT, name=jobName2, 
    nodalOutputPrecision=SINGLE, numCpus=1, numDomains=1, 
    parallelizationMethodExplicit=DOMAIN, scratch='', type=ANALYSIS, 
    userSubroutine='')
os.chdir(tDr)
try:
	mdb.jobs[jobName2].submit(consistencyChecking=OFF)
	mdb.jobs[jobName2].waitForCompletion()
	os.chdir(wDr)
except: pass

os.chdir(wDr)
execfile('Pois-Eval.py')
if saveFig==1:
	execfile('All-Fig.py')
if saveMov==1:
	execfile('Pois-Movie.py')
