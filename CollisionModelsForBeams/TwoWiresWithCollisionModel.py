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
        showCollisionModels = 1
        useBeamElements = 1 
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
        radiusSphereCollisionModel = str(0.95 * radius)
        # heigth of the strand 
        h = 2
        # number of nodes
        nn = 10
        nbeam = nn - 1
        # topology
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        lines = str(lines.flatten()).replace('[', '').replace(']','')

        BC = 'AxialForceAtTip'# 'MoveNodeAtTip'

        x, q = ParametricHelix.getCoordPointsAlongHellix(0, h, nn, tmax = 0.5 * np.pi)
        if useBeamElements:
            number_dofs_per_node = 7
        else:
            number_dofs_per_node = 3

        Coord = np.zeros((nn, number_dofs_per_node),dtype=float)
        Coord[:, :3] = x 
        if useBeamElements:
            Coord[:, 3:] = q
        # import pdb; pdb.set_trace()
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')

        # rootNode/beamI --> straight beam
        beamI = rootNode.createChild('beamI')
        self.beamI = beamI
        beamI.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beamI.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beamI.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beamI.createObject('MeshTopology', lines=lines, name='lines')
        beamI.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beamI.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beamI.createObject('BeamFEMForceField', radius=str(radius), name='FEM', poissonRatio='0.49', youngModulus='20000000')
        # beamI.createObject('MeshSpringForceField', name='Springs', stiffness='450000', template='Vec3d')
        Collision = beamI.createChild('Collision')
        self.Collision = Collision
        beamI.createObject('SphereModel', radius=radiusSphereCollisionModel, name='SphereCollision')

        # rootNode/beamJ --> helicoidal beam
        Coord = np.zeros((nn, 7),dtype=float)
        x, q = ParametricHelix.getCoordPointsAlongHellix(2 * radius, h, nn, tmax = 0.5 * np.pi)
        Coord[:,:3] = x 
        Coord[:, 3:] = q
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        beamJ = rootNode.createChild('beamJ')
        self.beamJ = beamJ
        beamJ.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beamJ.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        # beamJ.createObject('MechanicalObject', position='0 -2 0.25 0 0 0 1 0 -1 0.25 0 0 0 1  0 0 0.25 0 0 0 1  0 1 0.25 0 0 0 1  0 2 0.25 0 0 0 1', name='DOFs', template='Rigid')
        beamJ.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beamJ.createObject('MeshTopology', lines=lines, name='lines')
        beamJ.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beamJ.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beamJ.createObject('BeamFEMForceField', radius=str(radius), name='FEM', poissonRatio='0.49', youngModulus='20000000')
        # beamJ.createObject('MeshSpringForceField', name='Springs', stiffness='450000', template='Vec3d')
        #beamJ.createObject('SphereModel', radius=radiusSphereCollisionModel, name='SphereCollision')
        Collision = beamJ.createChild('Collision')
        self.Collision = Collision
        # Collision.createObject('CubeTopology', nx='15', ny='2', nz='2', min='0 -0.1 -0.1', max='7 0.1 0.1', printLog='True', drawEdges='True')
        Collision.createObject('CubeTopology',  printLog='True', drawEdges='True')

        if BC == 'AxialForceAtTip':
            #index of the last node
            index = str(nn-1)
            beamI.createObject('ConstantForceField', indices=index, showArrowSize='0.0005', printLog='1', forces='0 0 1000 0 0 0')
            beamJ.createObject('ConstantForceField', indices=index, showArrowSize='0.0005', printLog='1', forces='0 0 1000 0 0 0')
        elif BC == 'MoveNodeAtTip':
            index = str(nn-1)
            # not implemented apparently 
            beamI.createObject('LinearMovementConstraint', keyTimes='0 10', template='Rigid3d', movements='0 0 0   0 0 0                 0 0 1   0 0 0', indices=index)
            beamJ.createObject('LinearMovementConstraint', keyTimes='0 10', template='Rigid3d', movements='0 0 0   0 0 0                 0 0 1   0 0 0', indices=index)
            
        else:
            raise NotImplementedError

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