#Made by J.T.B. Overvelde on 9 may 2011

rep=0
while os.path.exists(tDr+'/'+jobName2+'.lck')==True:
	time.sleep(1)
	rep=rep+1
	if rep>30:
		break

odb = openOdb(path=tDr+'/'+jobName2+'.odb')

#calculate poisson ratio
text_file = open("Output-PoisAll.txt", "w")
nFrames=len(odb.steps[stepName2].frames)
for i in range(1,nFrames):
	lastFrame = odb.steps[stepName2].frames[i]
	displacement=lastFrame.fieldOutputs['U']
	RForce=lastFrame.fieldOutputs['RF']
	regS1 = odb.rootAssembly.instances[instRefName1].nodeSets['VIRTUAL1']
	regS2 = odb.rootAssembly.instances[instRefName2].nodeSets['VIRTUAL2']
	eps11 = displacement.getSubset(region=regS1).values[0].data[0]/(GridSpaceX*numHolesX)
	eps22 = displacement.getSubset(region=regS2).values[0].data[1]/(GridSpaceY*numHolesY)
	delta22 = displacement.getSubset(region=regS2).values[0].data[1]
	F22 = RForce.getSubset(region=regS2).values[0].data[1]
	v=-eps11/eps22
	#write to text file
	text_file.write('%1.10f %1.10f %1.10f %1.10f %1.10f %1.10f\n' % (v,-eps22+ec,-eps22,F22/(GridSpaceX*numHolesX),F22,delta22))
text_file.close()

odb.close()

#save eigenvalues
odb = openOdb(path=tDr+'/'+jobName1+'.odb')
nFrames=len(odb.steps[stepName1].frames)
text_file = open("Output-PoisMode.txt", "w")
for i in range(1,nFrames):
	lastFrame = odb.steps[stepName1].frames[i]
	n=len(lastFrame.description)
	for j in range(9,15):
		try:
			Val=float(lastFrame.description[n-j:n])
		except: pass
	text_file.write('%1.5f\n' % (Val/(numHolesY*GridSpaceY)))
text_file.close()
odb.close()









































