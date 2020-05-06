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
import ParametricHelix
import numpy as np
from pyquaternion import Quaternion

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
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')

        # radius of the beam
        radius = 0.1
        # number of nodes
        nn = 5
        nbeam = nn - 1
        # topology
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        # convert to string
        lines = str(lines.flatten()).replace('[', '').replace(']','')

        # position of the nodes
        Coord = np.zeros((nn, 7),dtype=float)
        x = np.zeros(nn,dtype=float)
        y = np.zeros(nn, dtype=float)
        z = np.zeros(nn, dtype=float)
        xp = np.zeros(nn,dtype=float)
        yp = np.zeros(nn, dtype=float)
        zp = np.zeros(nn, dtype=float)
        # coefficients of the equation of a titled straight line
        a = 1
        b = 1 
        c = 1
        t = np.linspace(0,1, nn)
        # components of the position vectors
        x = a * t 
        y = b * t 
        z = c * t 
        # components of the field of tangent vectors 
        xp = a 
        yp = b 
        zp = c 
        nrm = np.sqrt(a**2 + b**2 + c**2)

        # https://math.stackexchange.com/a/476311/392320
        q = np.zeros((nn,4), dtype = float)
        a = np.array([1,0,0])
        # vector connecting the two nodes of the future beam
        b = np.array([xp, yp, zp])/nrm
        v = np.cross(a,b)
        s = np.linalg.norm(v) 
        
        if not np.allclose(s, 0):
            c = np.dot(a,b)
            vskew = np.array([[0, -v[2], v[1]], [v[2], 0 , -v[0]], [-v[1], v[0], 0]  ])
            # rotation matrix rotating a into b
            R = np.eye(3) + vskew + np.dot(vskew, vskew) * ((1-c)/(s**2))
        else:
            R = np.eye(3)
        try:
            assert np.allclose(R.dot(a), b)
        except AssertionError:
            import pdb; pdb.set_trace()
        qii = Quaternion(matrix=R).elements
        # reorder the order of the components of the quaternion 
        # in pyquaternion: wxyz
        # in sofa: xyzw --> https://www.sofa-framework.org/api/master/sofa/html/classsofa_1_1helper_1_1_quater.html
        # qfinal = [q[1], q[2], q[3], q[0]]
        qi= Quaternion(axis=[0,0,1], radians=0.25 * np.pi)
        # import pdb; pdb.set_trace()
        qfinal = [qii[1], qii[2], qii[3], qii[0]]
        # import pdb; pdb.set_trace()
        # qfinal = [0, 0, 1, 0.25 * np.pi]
        q[:] = qfinal
        # q[0] = [0, 0, 1, 0.25 * np.pi] 

        Coord[:,0] = x
        Coord[:,1] = y
        Coord[:,2] = z
        Coord[:, 3:] = q 
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')

        # rootNode/beamI --> straight beam
        beamI = rootNode.createChild('beamI')
        self.beamI = beamI
        beamI.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beamI.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        # beamI.createObject('MechanicalObject', position=strCoord, rotation='0 0 45', name='DOFs', template='Rigid3d')
        beamI.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beamI.createObject('MeshTopology', lines=lines, name='lines')
        beamI.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beamI.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beamI.createObject('BeamFEMForceField', radius=radius, name='FEM', poissonRatio='0.49', youngModulus='1000')

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