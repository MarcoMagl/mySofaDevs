"""
BeamFEMForceFieldPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted/BeamFEMForceField.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted/BeamFEMForceFieldPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa
import numpy as np
from pyquaternion import Quaternion

def getCoordPointsAlongHellix(r, h, npt, tmax):
    # position vectors along the curve
    x = np.zeros((npt,3), dtype = float)
    # tangent vectors
    xp = np.zeros((npt,3), dtype = float)
    t = np.linspace(0,tmax, npt)
    x[:,0] = r * np.cos(t)
    x[:,1] = r * np.sin(t)
    x[:,2] = h * t

    xp[:,0] = -r * np.sin(t)
    xp[:,1] = r * np.cos(t)
    xp[:,2] = h 

    # quaternions
    q = np.zeros((npt,4), dtype = float)
    a = np.array([1,0,0])
    # trick: find the rotation matrix rotating global basis vector a into tangent vector b
    # extract the associated quaternion
    for i in range(npt):
        #tangent to the curve at the node
        b = xp[i]/np.linalg.norm(xp[i])
        assert np.allclose(np.linalg.norm(b), 1.)
        v = np.cross(a,b)
        s = np.linalg.norm(v) 
        if not np.allclose(s, 0):
            c = np.dot(a,b)
            vskew = np.array([[0, -v[2], v[1]], [v[2], 0 , -v[0]], [-v[1], v[0], 0]  ])
            # rotation matrix rotating a into b
            R = np.eye(3) + vskew + np.dot(vskew, vskew) * ((1-c)/(s**2))
        else:
            R = np.eye(3)
        assert np.allclose(R.dot(a), b)
        # extract the quaternion
        qi = Quaternion(matrix=R).elements
        # components provided by pyquaternion are not in the same order 
        # as the one expected by the constructor of Quater in SOFA
        # we must reorder them
        q[i]= [qi[1], qi[2], qi[3], qi[0]]

    return x, q


class BeamFEMForceField (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):
        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        showCollisionModels = 0
        if showCollisionModels:
            rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        else:
            rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')
        rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.02', alarmDistance='0.03', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='default')

        # radius of the beam
        radius = 0.1
        radiusSphereCollisionModel = str(1. * radius)
        # heigth of the strand 
        h = 2

        # rootNode/beamI --> straight beam
        nn = 5
        nbeam = nn - 1
        Coord = np.zeros((nn, 7),dtype=float)
        Coord[:,0] = 0
        Coord[:,1] = 0 
        Coord[:,2] = np.linspace(0,h,nn)
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        # topology
        lines = str(lines.flatten()).replace('[', '').replace(']','')
        x, q = getCoordPointsAlongHellix(0, h, nn, tmax = 0.5 * np.pi)
        Coord[:, 3:] = q
        # import pdb; pdb.set_trace()
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        beamI = rootNode.createChild('beamI')
        self.beamI = beamI
        beamI.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beamI.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beamI.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beamI.createObject('MeshTopology', lines=lines, name='lines')
        beamI.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beamI.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beamI.createObject('BeamFEMForceField', radius=str(radius), name='FEM', poissonRatio='0.49', youngModulus='20000000')
        Collision = beamI.createChild('Collision')
        self.Collision = Collision
        beamI.createObject('SphereModel', radius=radiusSphereCollisionModel, name='SphereCollision')

        # rootNode/beam2 --> helicoidal beam
        nn = 10 
        nbeam = nn - 1
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        # topology
        lines = str(lines.flatten()).replace('[', '').replace(']','')
        Coord = np.zeros((nn, 7),dtype=float)
        x, q = getCoordPointsAlongHellix(2 * radius, h, nn, tmax = 0.5 * np.pi)
        Coord[:,:3] = x 
        Coord[:, 3:] = q
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        beam2 = rootNode.createChild('beam2')
        self.beam2 = beam2
        beam2.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beam2.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        # beam2.createObject('MechanicalObject', position='0 -2 0.25 0 0 0 1 0 -1 0.25 0 0 0 1  0 0 0.25 0 0 0 1  0 1 0.25 0 0 0 1  0 2 0.25 0 0 0 1', name='DOFs', template='Rigid')
        beam2.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beam2.createObject('MeshTopology', lines=lines, name='lines')
        beam2.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beam2.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beam2.createObject('BeamFEMForceField', radius=str(radius), name='FEM', poissonRatio='0.49', youngModulus='20000000')
        beam2.createObject('SphereModel', radius=radiusSphereCollisionModel, name='SphereCollision')

        return 0;

    def onMouseButtonLeft(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Left mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onKeyReleased(self, c):
        ## usage e.g.
        #if c=="A" :
        #    print "You released a"
        return 0;

    def initGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onKeyPressed(self, c):
        ## usage e.g.
        #if c=="A" :
        #    print "You pressed control+a"
        return 0;

    def onMouseWheel(self, mouseX,mouseY,wheelDelta):
        ## usage e.g.
        #if isPressed : 
        #    print "Control button pressed+mouse wheel turned at position "+str(mouseX)+", "+str(mouseY)+", wheel delta"+str(wheelDelta)
        return 0;

    def storeResetState(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = '0.01'
    rootNode.findData('gravity').value = '0 0 -9.81'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myBeamFEMForceField = BeamFEMForceField(rootNode,commandLineArguments)
    return 0;