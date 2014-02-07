#Made by J.T.B. Overvelde on 9 may 2011

mdb.models[modelName1].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models[modelName1].rootAssembly.Instance(dependent=ON, name=instName1, 
    part=mdb.models[modelName1].parts[partName1])

mdb.models[modelName1].rootAssembly.Instance(dependent=ON, name=
    instRefName1, part=mdb.models[modelName1].parts[refName1])
mdb.models[modelName1].rootAssembly.Instance(dependent=ON, name=
    instRefName2, part=mdb.models[modelName1].parts[refName2])

mdb.models[modelName1].parts[refName1].Set(name='VIRTUAL1', 
    referencePoints=(
    mdb.models[modelName1].parts[refName1].referencePoints[1], ))
mdb.models[modelName1].parts[refName2].Set(name='VIRTUAL2', 
    referencePoints=(
    mdb.models[modelName1].parts[refName2].referencePoints[1], ))
mdb.models[modelName1].rootAssembly.regenerate()
