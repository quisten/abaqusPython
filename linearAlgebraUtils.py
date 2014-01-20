"""
#=====================================================
#	      file:  utils.py
#     written by:  James Lockley 
#  last modified:  July 18th 2003	
#
#    Description: a series of frequently used functions
#                 to perform vector algebra 
#                 
#!!!!!!  CAUTION: Check functions to your own satisfaction  !!!!!!
#  			no warranty of validity! 	
#                 
#=======================================================
"""

import math
from math import cos, sin, pi, sqrt
from Numeric import array, matrixmultiply, dot


######################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def crossproduct(vectorA,vectorB):
    """ crossproduct(vectorA,vectorB) --> returns the crossproduct of vectorA, vectorB"""
    xproduct=[None, None, None]
    xproduct[0]=vectorA[1]*vectorB[2]-vectorA[2]*vectorB[1]
    xproduct[1]=vectorA[2]*vectorB[0]-vectorA[0]*vectorB[2]
    xproduct[2]=vectorA[0]*vectorB[1]-vectorA[1]*vectorB[0]
    return xproduct
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def vectorDifference(first, second):
    """ vectorDifference(first, second) --> returns difference 
        components of arbitary length vectors"""
    try:
	    vector = [first[0]-second[0], first[1]-second[1], first[2]-second[2]]
    except:
            print first, second
            1/0
    return vector
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def vectorAdd(first, second):
    """vectorAdd(first, second) --> adds components of 2 vectors"""
    vector = [first[0]+second[0], first[1]+second[1], first[2]+second[2]]
    return vector
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def scalarMultiply(scalar, vector):
    """ scalarMultiply(scalar, vector) --> multiplies components of vector by scalar"""

    return [vector[0]*scalar, vector[1]*scalar, vector[2]*scalar]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def magnitude(vector):
    """magnitude(vector) --> gives magnitude of vector"""
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def normalise(vector):
    """normalise(vector) --> normalises given vector"""
    length = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    vector = [vector[0]/length,vector[1]/length,vector[2]/length]
    return vector

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calculateSRSS(x,y,z):
    """calculateSRSS(x,y,z) --> returns the 'SquareRoot of Sum of Squares' 
       of three numbers."""

    return math.sqrt(x**2 + y**2 + z**2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rotatePoint(coord, angle, axis, arcCentre):
    """ rotates point around axis through arcCentre"""
    tmpCoord = vectorDifference(coord, arcCentre)
    rotCoord = arbitaryRotation(tmpCoord, angle, axis)
    newCoord = vectorAdd(rotCoord, arcCentre)
    return newCoord

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def arbitaryRotation(coord, angle, axis):
    """arbitaryRotation(coord, angle, vector) -->  rotates point by angle around vector
       !!NB!! the axis is always through the origin!! must do offset first"""

    u, v, w = normalise(axis)
    oldCoord = array([coord[0], coord[1], coord[2]])
    cth = cos(angle/180.*pi)
    sth = sin(angle/180.*pi)

    R = array([[cth + u**2*(1-cth), -w*sth+u*v*(1-cth),  v*sth+u*w*(1-cth)],
	       [ w*sth+u*v*(1-cth),   cth+v**2*(1-cth), -u*sth+v*w*(1-cth)],
	       [-v*sth+u*w*(1-cth),  u*sth+v*w*(1-cth),   cth+w**2*(1-cth)]])

    newCoord = matrixmultiply(R,oldCoord)
    return [newCoord[0], newCoord[1], newCoord[2]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def intersection(point1, vector1, point2, vector2):
    """intersection(point1, vector1, point2, vector2) 
       --> returns the coords of the intersection of 2 lines in space - 
       assuming lines will intersect!! - no error checking yet..."""
       
    a1, a2, a3 = point1
    b1, b2, b3 = vector1
    c1, c2, c3 = point2
    d1, d2, d3 = vector2

    # need try statements as if section lies in a plane, will get
    # divide by zero on 2 of the 3 solutions for t
    try:
	t = ((-a3 + c3)*d2 + (a2 - c2)*d3)/(b3*d2 - b2*d3)
    except:
	try:
	    t = ((-a1 + c1)*d2 + (a2 - c2)*d1)/(b1*d2 - b2*d1)
	except:
	    t = ((-a1 + c1)*d3 + (a3 - c3)*d1)/(b1*d3 - b3*d1)

    intersection = [a1 + b1*t, a2 + b2*t, a3 + b3*t]
    intersection = setZero(intersection)
    return intersection


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parallel(linevector, linePointOn, planePointOn,  planeNormal, offset):
    """ parallel(linevector, linePointOn, planePointOn,  planeNormal, offset) -->
        gives coordinates of point on the plane defined by planeNormal
        and linePointOn, through which a line will run  || to linevector
	but offset by offset and on the same side of the line as planePointOn.
	planePointOn need not lie on the plane, but the nearer the better..."""

    perpendicular = normalise(crossproduct(linevector, planeNormal))

    # decide if perpendicular is in the general direction of planePointOn
    vector = vectorDifference(planePointOn, linePointOn)
    dotP = dot(perpendicular, vector)

    if dotP > 0: 
	sign =+1
    else:
	sign =-1

    offsetV = scalarMultiply((sign*offset), perpendicular)
    return vectorAdd(offsetV, linePointOn)

    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setZero(vector):
    """ setZero(vector) --> if indivual components of the vector are 
        less than 1e-6 --> sets it to zero"""

    for i in range(len(vector)):
	if abs(vector[i]) < 1e-6: vector[i]= 0.
    return vector

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def projectPointOntoPlane(point, planeNormal, planePoint):
    planeNormal = normalise(planeNormal)
    relVector = vectorDifference(planePoint, point)
    dist = dot(relVector,planeNormal)
    oldpoint =point

    point = vectorAdd(point, (scalarMultiply(dist, planeNormal)))

    return point

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def copyRotateNode(offset, numCircum, centreCoord, vector, lastNewNodeLabel):

    """copyRotateNode(numCircum, centreCoord, vector, nodeList, lastNewNodeLabel)
       --> copy and rotate ring of nodes around centre node"""

    coord = vectorAdd(offset, centreCoord) 
    nodeList=[coord]
    angle = 360./numCircum
    for num in range(numCircum):
	""" as the axis of rotation is the vector difference 
	of A and B, the vector passes through the origin, must
	use offset from the axis instead of abs coords""" 

	offset = vectorDifference(nodeList[-1],  centreCoord)
	coord = arbitaryRotation(offset, angle, vector)
	coord = setZero(coord)
	coord = vectorAdd(coord, centreCoord) 
	nodeList.append(coord)

    for i in range(len(nodeList)):
	nodeList[i].insert(0,lastNewNodeLabel)
	newNodeLabels.append(lastNewNodeLabel)
	lastNewNodeLabel = lastNewNodeLabel + 1


    return nodeList, lastNewNodeLabel

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~