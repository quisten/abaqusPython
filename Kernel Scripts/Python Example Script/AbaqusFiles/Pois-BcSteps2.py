#Made by J.T.B. Overvelde on 9 may 2011

#copy model and delete old steps
mdb.Model(name=modelName2, objectToCopy=mdb.models[modelName1])
del mdb.models[modelName2].steps[stepName1]

#steps
mdb.models[modelName2].StaticStep(nlgeom=ON, initialInc=maxIncr, minInc=1e-6, 
    maxInc=maxIncr, maxNumInc=maxNumIncr, name=stepName2, previous='Initial',
    contactSolutions=10,contactIterations=300,applyContactIterations=True)

#BC
mdb.models[modelName2].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName2, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-1', region=
    mdb.models[modelName1].rootAssembly.instances[instRefName1].sets['VIRTUAL1']
    , u1=UNSET, u2=0.0, ur3=UNSET)
mdb.models[modelName2].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName2, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-2', region=
    mdb.models[modelName1].rootAssembly.instances[instRefName2].sets['VIRTUAL2'] 
    , u1=0.0, u2=UNSET, ur3=UNSET)
mdb.models[modelName2].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName2, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-3', region=
    mdb.models[modelName1].rootAssembly.instances[instRefName2].sets['VIRTUAL2']
    , u1=UNSET, u2=-stepSize*GridSpaceY*numHolesY, ur3=UNSET)
mdb.models[modelName2].DisplacementBC(amplitude=UNSET, buckleCase=
    PERTURBATION_AND_BUCKLING, createStepName=stepName2, distributionType=
    UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='BC-4', region=
    mdb.models[modelName1].rootAssembly.instances[instName1].sets['vertic3'], 
    u1=0, u2=0, ur3=UNSET)

#contact
mdb.models[modelName2].ContactProperty('IntProp-1')
mdb.models[modelName2].interactionProperties['IntProp-1'].NormalBehavior(
	    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
	    pressureOverclosure=HARD)
for i in range(0,len(CenSide)):
	mdb.models[modelName2].SelfContactStd(createStepName=stepName2, 
    	    interactionProperty='IntProp-1', name='Int-'+str(i), smooth=0.2, surface=
    	    mdb.models[modelName2].rootAssembly.instances[instName1].surfaces['Surf-'+str(i)])

#apply imperfection
odb = openOdb(path=tDr+'/'+jobName1+'.odb')
Frame1 = odb.steps[stepName1].frames[1]
displacement=Frame1.fieldOutputs['U']
fieldValues=displacement.values
Coor=zeros((len(mdb.models[modelName2].parts[partName1].nodes),3),Float)
rep=0
for i in mdb.models[modelName2].parts[partName1].nodes:
	Coor[i.label-1][0]=i.coordinates[0]+imperf*fieldValues[i.label-1].data[0]
	Coor[i.label-1][1]=i.coordinates[1]+imperf*fieldValues[i.label-1].data[1]
	Coor[i.label-1][2]=0.0
	rep=rep+1
mdb.models[modelName2].parts[partName1].editNode(
    nodes=mdb.models[modelName2].parts[partName1].nodes,
    coordinates=Coor)
odb.close()
