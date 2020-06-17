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
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.02', alarmDistance='0.03', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='default')

        radius = 0.1
        startWithPenetration = 1
        PenetrationWanted = 0.1 * radius
        if startWithPenetration:
            radiusSphereCollisionModel = str(radius + 0.5 * PenetrationWanted)
        else:
            radiusSphereCollisionModel = str(1. * radius)
        secondBeam = 1
        # for the cube topology collision objects
        xminBI = -2
        xmaxBI = 2
        yminBI = - radius
        ymaxBI = + radius
        zminBI = - radius
        zmaxBI = + radius

        bvminBI = str(xminBI) + ' ' + str(yminBI) + ' ' + str(zminBI)
        bvmaxBI = str(xmaxBI) + ' ' + str(ymaxBI) + ' ' + str(zmaxBI)

        q = [0, 0, 0, 1]
        nn = 5
        import numpy as np
        Coord = np.zeros((nn, 7),dtype=float)
        Coord[:,0] = np.linspace(-2,2, nn)
        Coord[:,1] = 1 
        Coord[:, 3:7,] = q
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')

        # rootNode/beamI
        beamI = rootNode.createChild('beamI')
        self.beamI = beamI
        beamI.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beamI.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beamI.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beamI.createObject('MeshTopology', lines='0 1 1 2 2 3 3 4', name='lines')
        beamI.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beamI.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beamI.createObject('BeamFEMForceField', radius=str(radius), name='FEM', poissonRatio='0.49', youngModulus='20000000')
        Collision = beamI.createChild('Collision')
        self.Collision = Collision
        beamI.createObject('SphereModel', radius=radiusSphereCollisionModel, name='SphereCollision')

        # rootNode/beam2
        # quaternion to orientate the beams in the y direction
        x = 0.7071067811865475
        q = [0, 0, x, x]
        nn = 5
        import numpy as np
        Coord = np.zeros((nn, 7),dtype=float)
        Coord[:,1] = np.linspace(-2,2, nn)
        Coord[:,2] = 0.25
        Coord[:, 3:7,] = q
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        beam2 = rootNode.createChild('beam2')
        self.beam2 = beam2
        beam2.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beam2.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        # beam2.createObject('MechanicalObject', position='0 -2 0.25 0 0 0 1 0 -1 0.25 0 0 0 1  0 0 0.25 0 0 0 1  0 1 0.25 0 0 0 1  0 2 0.25 0 0 0 1', name='DOFs', template='Rigid')
        beam2.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beam2.createObject('MeshTopology', lines='0 1 1 2 2 3 3 4', name='lines')
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