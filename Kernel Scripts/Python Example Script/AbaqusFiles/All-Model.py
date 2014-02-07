#Made by J.T.B. Overvelde on 9 may 2011

###create model###

#create model
mdb.models.changeKey(fromName='Model-1', toName=modelName1)

###create parts###

#create part
mdb.models[modelName1].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models[modelName1].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(numHolesX*GridSpaceX, numHolesY*GridSpaceY))
mdb.models[modelName1].Part(dimensionality=TWO_D_PLANAR, name=partName1, type=
    DEFORMABLE_BODY)
mdb.models[modelName1].parts[partName1].BaseShell(sketch=
    mdb.models[modelName1].sketches['__profile__'])
del mdb.models[modelName1].sketches['__profile__']
mdb.models[modelName1].ConstrainedSketch(gridSpacing=0.1, name='__profile__'
    , sheetSize=10)
#create Virtual nodes (reference nodes)
mdb.models[modelName1].Part(dimensionality=TWO_D_PLANAR, name=refName1, 
    type=DEFORMABLE_BODY)
mdb.models[modelName1].parts[refName1].ReferencePoint(point=(0.0, 
    0.0, 0.0))
mdb.models[modelName1].Part(dimensionality=TWO_D_PLANAR, name=refName2, 
    type=DEFORMABLE_BODY)
mdb.models[modelName1].parts[refName2].ReferencePoint(point=(0.0, 
    0.0, 0.0))
#create center of holes
arCenX=zeros([numHolesX*numHolesY+1],Float)
arCenY=zeros([numHolesX*numHolesY+1],Float)
n=0
x=-GridSpaceX
for a in range(0, numHolesX):
	x=x+GridSpaceX
	y=-GridSpaceY
	for b in range(0, numHolesY):
	    	y=y+GridSpaceY
		n=n+1
		arCenX[n]=x
		arCenY[n]=y
#make sketches
InstCen=[]
for i in range(0,nS):
	mdb.models[modelName1].ConstrainedSketch(gridSpacing=0.1, name='__profile__'
            , sheetSize=10)
	mdb.models[modelName1].parts[partName1].projectReferencesOntoSketch(filter=
	    COPLANAR_EDGES, sketch=mdb.models[modelName1].sketches['__profile__'])
	mdb.models[modelName1].sketches['__profile__'].Spline(points=(vars()['valSpline'+str(i+1)]))
	mdb.models[modelName1].ConstrainedSketch(name='Sketch'+str(i), objectToCopy=
	    mdb.models[modelName1].sketches['__profile__'])
	del mdb.models[modelName1].sketches['__profile__']
	a=vars()['valSpline'+str(i+1)]
	sumaX=0
	sumaY=0
	for j in range(0,len(a)):
		sumaX=sumaX+a[j][0]/len(a)
		sumaY=sumaY+a[j][1]/len(a)
	InstCen=InstCen+[(sumaX,sumaY)]
#extrude sketches
mdb.models[modelName1].ConstrainedSketch(gridSpacing=0.1, name='__profile__'
            , sheetSize=10)
mdb.models[modelName1].parts[partName1].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models[modelName1].sketches['__profile__'])
CenExist=[]
CenSide=[]
for i in range(1,numHolesX*numHolesY+1):
	for j in range(0,nS):
		stop=0
		
		for k in range(0,len(CenExist)):
			if round(fac*(arCenX[i]-arCenX[1]+InstCen[j][0]))==round(fac*CenExist[k][0]) and round(fac*
			    (arCenY[i]-arCenY[1]+InstCen[j][1]))==round(fac*CenExist[k][1]):
				stop=1
		if stop==0:
			mdb.models[modelName1].sketches['__profile__'].retrieveSketch(sketch=
		    	    mdb.models[modelName1].sketches['Sketch'+str(j)])
			mdb.models[modelName1].sketches['__profile__'].move(objectList=(
		    	    mdb.models[modelName1].sketches['__profile__'].geometry.findAt(vars()['valSpline'
			    +str(j+1)][1], ), ),vector=(arCenX[i]-arCenX[1], arCenY[i]-arCenY[1]))	
			CenExist=CenExist+[(arCenX[i]-arCenX[1]+InstCen[j][0],arCenY[i]-arCenY[1]+InstCen[j][1])]
			b=vars()['valSpline'+str(j+1)]
			c=zeros(2,Float)
			c[0]=b[0][0]+arCenX[i]-arCenX[1]
			c[1]=b[0][1]+arCenY[i]-arCenY[1]
			rep=0
			while c[0]<0 or c[0]>GridSpaceX*numHolesX or c[1]<0 or c[1]>GridSpaceY*numHolesY:
				rep=rep+1
				c[0]=b[rep][0]+arCenX[i]-arCenX[1]
				c[1]=b[rep][1]+arCenY[i]-arCenY[1]
			CenSide=CenSide+[(c[0],c[1])]
mdb.models[modelName1].parts[partName1].Cut(sketch=
    mdb.models[modelName1].sketches['__profile__'])
del mdb.models[modelName1].sketches['__profile__']

###sets for edge and vertices###

#make edge sets for part (left,right,top,bottom)
LEdges=[]; REdges=[]; TEdges=[]; BEdges=[]
for i in mdb.models[modelName1].parts[partName1].edges:
	a=i.pointOn[0]
	if round(a[0]*fac)==0:
		LEdges=LEdges+[mdb.models[modelName1].parts[partName1].edges.findAt(((a[0],a[1],a[2]),))]
	elif round(a[0]*fac)==round(numHolesX*GridSpaceX*fac):
		REdges=REdges+[mdb.models[modelName1].parts[partName1].edges.findAt(((a[0],a[1],a[2]),))]
	elif round(a[1]*fac)==round(numHolesY*GridSpaceY*fac):
		TEdges=TEdges+[mdb.models[modelName1].parts[partName1].edges.findAt(((a[0],a[1],a[2]),))]
	elif round(a[1]*fac)==0:
		BEdges=BEdges+[mdb.models[modelName1].parts[partName1].edges.findAt(((a[0],a[1],a[2]),))]	
mdb.models[modelName1].parts[partName1].Set(edges=LEdges, name='SL')
mdb.models[modelName1].parts[partName1].Set(edges=REdges, name='SR')
mdb.models[modelName1].parts[partName1].Set(edges=TEdges, name='TOP')
mdb.models[modelName1].parts[partName1].Set(edges=BEdges, name='BOTTOM')
#make vertices sets for part
rep=1
for i in mdb.models[modelName1].parts[partName1].vertices:
	a=i.pointOn[0]
	if round(a[0]*fac)==0:
		LVertic=[mdb.models[modelName1].parts[partName1].vertices.findAt(((a[0],a[1],a[2]),))]
		mdb.models[modelName1].parts[partName1].Set(vertices=LVertic, name='vertic'+str(rep))
		rep=rep+1
	elif round(a[0]*fac)==round(numHolesX*GridSpaceX*fac):
		RVertic=[mdb.models[modelName1].parts[partName1].vertices.findAt(((a[0],a[1],a[2]),))]
		mdb.models[modelName1].parts[partName1].Set(vertices=RVertic, name='vertic'+str(rep))
		rep=rep+1

###materials###

mdb.models[modelName1].Material(name=matName)
mdb.models[modelName1].materials[matName].Hyperelastic(table=((mu/2.0, 
    2.0/K), ), testData=OFF, type=NEO_HOOKE, volumetricResponse=
    VOLUMETRIC_DATA)
mdb.models[modelName1].materials[matName].Density(table=((rho, ), ))
mdb.models[modelName1].HomogeneousSolidSection(material=matName, name=
    secName, thickness=None)

###sections###

mdb.models[modelName1].parts[partName1].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=mdb.models[modelName1].parts[partName1].faces.getSequenceFromMask(
    mask=('[#1 ]', ), )), sectionName=secName)

###mesh###

mdb.models[modelName1].parts[partName1].setMeshControls(elemShape=TRI, regions=
    mdb.models[modelName1].parts[partName1].faces.getSequenceFromMask(('[#1 ]', 
    ), ))
mdb.models[modelName1].parts[partName1].setElementType(elemTypes=(ElemType(
    elemCode=CPE8R, elemLibrary=STANDARD), ElemType(elemCode=CPE6H, 
    elemLibrary=STANDARD, distortionControl=DEFAULT)), regions=(
    mdb.models[modelName1].parts[partName1].faces.getSequenceFromMask(('[#1 ]', 
    ), ), ))
mdb.models[modelName1].parts[partName1].seedPart(deviationFactor=devMesh, size=sizeMesh)
LoopOver=[('SL',1),('SR',1),('TOP',0),('BOTTOM',0)]
for k in range(0,4):
	LO3=1
	if LoopOver[k][1]==1:
		LO3=0
	for i in mdb.models[modelName1].parts[partName1].sets[LoopOver[k][0]].edges:
		coor=[]; VCoorD=[]
		a=i.pointOn[0][LoopOver[k][1]]
		b=i.pointOn[0][LO3]
		for j in mdb.models[modelName1].parts[partName1].vertices:
			if j.pointOn[0][LO3]==b:
				VCoorD=VCoorD+[abs(abs(j.pointOn[0][LoopOver[k][1]])-a)]
		VCoorD.sort()
		nN=int(round(((VCoorD[0]+VCoorD[1])/sizeMesh)))
		mdb.models[modelName1].parts[partName1].seedEdgeByNumber(edges=[i], number=nN)
mdb.models[modelName1].parts[partName1].generateMesh()
mdb.models[modelName1].rootAssembly.regenerate()

###node sets for periodic constraints###

#left wall
a=[]
for i in mdb.models[modelName1].parts[partName1].sets['SL'].nodes:
	a=a+[(i.coordinates[1],i.label)]
a.sort()
rep=1
for i in a:
	mdb.models[modelName1].parts[partName1].Set(name='Node-'+str(rep), nodes=
	    mdb.models[modelName1].parts[partName1].nodes[(i[1]-1):(i[1])])
	rep=rep+2
#right wall
a=[]
for i in mdb.models[modelName1].parts[partName1].sets['SR'].nodes:
	a=a+[(i.coordinates[1],i.label)]
a.sort()
rep=2
for i in a:
	mdb.models[modelName1].parts[partName1].Set(name='Node-'+str(rep), nodes=
	    mdb.models[modelName1].parts[partName1].nodes[(i[1]-1):(i[1])])
	rep=rep+2
LenAV=len(a)
#bottom wall
a=[]
for i in mdb.models[modelName1].parts[partName1].sets['BOTTOM'].nodes:
	a=a+[(i.coordinates[0],i.label)]
a.sort()
rep=2*LenAV+1
for i in a:
	mdb.models[modelName1].parts[partName1].Set(name='Node-'+str(rep), nodes=
	    mdb.models[modelName1].parts[partName1].nodes[(i[1]-1):(i[1])])
	rep=rep+2
#top wall
a=[]
for i in mdb.models[modelName1].parts[partName1].sets['TOP'].nodes:
	a=a+[(i.coordinates[0],i.label)]
a.sort()
rep=2*LenAV+2
for i in a:
	mdb.models[modelName1].parts[partName1].Set(name='Node-'+str(rep), nodes=
	    mdb.models[modelName1].parts[partName1].nodes[(i[1]-1):(i[1])])
	rep=rep+2
LenAH=len(a)

#create surfaces for contact
for a in range(0,len(CenSide)):
	nameSurf='Surf-'+str(a)		
	mdb.models[modelName1].parts[partName1].Surface(name=nameSurf, side1Edges=
    	    mdb.models[modelName1].parts[partName1].edges.findAt(((CenSide[a][0], 
	    CenSide[a][1], 0), )))

