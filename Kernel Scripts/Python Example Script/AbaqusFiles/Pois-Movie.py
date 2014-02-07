#Made by J.T.B. Overvelde on 9 may 2011

os.chdir(tDr)

# Create a new vieport for this example.
myViewport=session.Viewport(name='MakeMov',
	origin=(0,0), width=300, height=200)
session.viewports['MakeMov'].makeCurrent()
session.viewports['MakeMov'].maximize()
session.viewports['MakeMov'].view.fitView()

# Open the output database and associate with the new viewportodbPath = jobName2+'.odb'
myOdb = visualization.openOdb(path=odbPath)
myViewport.setValues(displayedObject=myOdb)
myViewport.odbDisplay.superimposeOptions.setValues(
    visibleEdges=NONE, translucencyFactor=0.15)
myViewport.odbDisplay.basicOptions.setValues(
    translucencySort=ON)
myViewport.odbDisplay.commonOptions.setValues(
    visibleEdges=NONE)
myViewport.odbDisplay.display.setValues(plotState=(
    UNDEFORMED, CONTOURS_ON_DEF, ))

#print
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'MakeMov', ))
session.imageAnimationOptions.setValues(vpDecorations=ON, vpBackground=OFF, 
    compass=OFF, timeScale=1, frameRate=12)
session.writeImageAnimation(fileName='Movie-Full', format=AVI, canvasObjects=(
    session.viewports['MakeMov'], ))

os.chdir(wDr)
myOdb.close()



