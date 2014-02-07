#Made by J.T.B. Overvelde on 9 may 2011

#execute
os.chdir(tDr)
mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
    SINGLE, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=
    modelName1, modelPrint=OFF, multiprocessingMode=DEFAULT, name=jobName1, 
    nodalOutputPrecision=SINGLE, numCpus=1, numDomains=1, 
    parallelizationMethodExplicit=DOMAIN, scratch='', type=ANALYSIS, 
    userSubroutine='')
mdb.jobs[jobName1].submit(consistencyChecking=OFF)
mdb.jobs[jobName1].waitForCompletion()
os.chdir(wDr)


