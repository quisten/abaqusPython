#Made by J.T.B. Overvelde on 9 may 2011

#constraints
rep=1
for i in range(0,LenAH):
	mdb.models[modelName1].Equation(name='Constraint-x-'+str(i+1), 
	    terms=((1.0, instName1+'.Node-'+str(rep), 1),(-1.0, instName1+'.Node-'+str(rep+1), 1), 
	    (1.0, instRefName1+'.VIRTUAL1', 1),(0, instRefName1+'.VIRTUAL1', 1)))
	rep=rep+2
rep=1
for i in range(0,LenAH):
	mdb.models[modelName1].Equation(name='Constraint-y-'+str(i+1), 
	    terms=((1.0, instName1+'.Node-'+str(rep), 2),(-1.0, instName1+'.Node-'+str(rep+1), 2), 
	    (1.0, instRefName1+'.VIRTUAL1', 2),(0, instRefName1+'.VIRTUAL1', 2)))
	rep=rep+2

val=1
test=mdb.models[modelName1].parts[partName1].vertices.findAt((0,0,0),)
if test==None:
	val=0

rep=2*LenAH+1+2*val
for i in range(LenAH,LenAV+LenAH-val):
	mdb.models[modelName1].Equation(name='Constraint-x-'+str(i+1), 
	    terms=((1.0, instName1+'.Node-'+str(rep), 1),(-1.0, instName1+'.Node-'+str(rep+1), 1), 
	    (1.0, instRefName2+'.VIRTUAL2', 1),(0, instRefName2+'.VIRTUAL2', 1)))
	rep=rep+2
	j=i+1
rep=2*LenAH+1+2*val
for i in range(LenAH,LenAV+LenAH-val):
	mdb.models[modelName1].Equation(name='Constraint-y-'+str(i+1), 
	    terms=((1.0, instName1+'.Node-'+str(rep), 2),(-1.0, instName1+'.Node-'+str(rep+1), 2), 
	    (1.0, instRefName2+'.VIRTUAL2', 2),(0, instRefName2+'.VIRTUAL2', 2)))
	rep=rep+2

#steps
mdb.models[modelName1].BuckleStep(maxIterations=200, name=stepName1, numEigen=1, previous='Initial')

#BC
mdb.models[modelName1].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName1, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-1', region=
    mdb.models[modelName1].rootAssembly.instances[instRefName1].sets['VIRTUAL1']
    , u1=UNSET, u2=0.0, ur3=UNSET)
mdb.models[modelName1].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName1, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-2', region=
    mdb.models[modelName1].rootAssembly.instances[instRefName2].sets['VIRTUAL2']
    , u1=0.0, u2=UNSET, ur3=UNSET)
mdb.models[modelName1].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName1, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-3', region=
    mdb.models[modelName1].rootAssembly.instances[instRefName2].sets['VIRTUAL2']
    , u1=UNSET, u2=-1.0, ur3=UNSET)
mdb.models[modelName1].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName1, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-4', region=
    mdb.models[modelName1].rootAssembly.instances[instName1].sets['vertic3'], 
    u1=0, u2=0, ur3=UNSET)
