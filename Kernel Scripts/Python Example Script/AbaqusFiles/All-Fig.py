os.chdir(tDr)

if routine==3:
	names=[(jobName1,stepName1),(jobName2,stepName2)]
	FrameNum=-1
if routine==4:
	names=[(jobName2,stepName1+'1')]
	FrameNum=1


for case in names:
	# Create a new vieport for this example.
	myViewport=session.Viewport(name='MakeFig',
		origin=(0,0), width=300, height=200)
	session.viewports['MakeFig'].makeCurrent()
	session.viewports['MakeFig'].maximize()
	session.viewports['MakeFig'].view.fitView()

	# Open the output database and associate with the new viewport	odbPath = case[0]+'.odb'
	myOdb = visualization.openOdb(path=odbPath)
	myViewport.setValues(displayedObject=myOdb)

	#Display a contour plot of the output database.
	myViewport.odbDisplay.display.setValues(plotState=(DEFORMED,))
	#Do not print the viewport decorations or Black background.
	session.printOptions.setValues(rendition=COLOR,
	vpDecorations=OFF, vpBackground=OFF)

	#print
#	numStep= myOdb.steps[case[1]]
#	nFrame=len(numStep.frames)
#	for m in range(0,nFrame):
#		numFrame = numStep.frames[m]
#		displacement=numFrame.fieldOutputs['U']
#		myViewport.odbDisplay.setFrame(step=numStep,frame=numFrame)
#		# Print the viewport to a local EPS-Format file.
#		session.printToFile('Figures/Fig-'+case[0]+'-'+case[1]+'-Frame-'+str(m),EPS,(myViewport,))
#	myOdb.close()
	
	numStep= myOdb.steps[case[1]]
	numFrame = numStep.frames[-1]
	displacement=numFrame.fieldOutputs['U']
	myViewport.odbDisplay.setFrame(step=numStep,frame=numFrame)
	# Print the viewport to a local EPS-Format file.
	os.chdir(wDr)
	session.printToFile('Figures/Fig_'+str(int(100*c1))+'_'+str(int(100*c2))+'_'+str(int(100*stepSize)),EPS,(myViewport,))
	os.chdir(tDr)
	myOdb.close()

os.chdir(wDr)
