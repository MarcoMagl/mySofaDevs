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

        # rootNode/beam
        beam = rootNode.createChild('beam')
        self.beam = beam
        beam.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beam.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beam.createObject('MechanicalObject', position='0 0 0 0 0 0 1  1 0 0 0 0 0 1  2 0 0 0 0 0 1  3 0 0 0 0 0 1  4 0 0 0 0 0 1  5 0 0 0 0 0 1  6 0 0 0 0 0 1  7 0 0 0 0 0 1', name='DOFs', template='Rigid')
        beam.createObject('Mesh', lines='0 1 1 2 2 3 3 4 4 5 5 6 6 7', name='lines')
        beam.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beam.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beam.createObject('BeamFEMForceField', radius='0.1', name='FEM', poissonRatio='0.49', youngModulus='20000000')

        # rootNode/beam/Collision
        Collision = beam.createChild('Collision')
        self.Collision = Collision
        Collision.createObject('CubeTopology', nx='15', ny='2', nz='2', min='0 -0.1 -0.1', max='7 0.1 0.1')
        Collision.createObject('MechanicalObject')
        Collision.createObject('BeamLinearMapping', isMechanical='true')
        Collision.createObject('TriangleCollisionModel')

        """
        # rootNode/beam2
        beam2 = rootNode.createChild('beam2')
        self.beam2 = beam2
        beam2.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beam2.createObject('CGLinearSolver', threshold='0.000000001', tolerance='0.0000000001', template='NewMat', iterations='25', printLog='false')
        beam2.createObject('MechanicalObject', position='0 0 1 0 0 0 1  1 0 1 0 0 0 1', name='DOFs', template='Rigid')
        beam2.createObject('Mesh', lines='0 1', name='lines')
        beam2.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beam2.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1')
        beam2.createObject('BeamFEMForceField', radius='0.05', name='FEM', poissonRatio='0.49', youngModulus='10000000')

        # rootNode/beam2/Collision2
        Collision2 = beam2.createChild('Collision2')
        self.Collision2 = Collision2
        Collision2.createObject('MechanicalObject')
        Collision2.createObject('SphereCollisionModel', position='0 0 0 0 0 0', radius='.2')
        Collision2.createObject('RigidMapping', index='1')
        """
        # rootNode/beam2
        beam2 = rootNode.createChild('beam2')
        self.beam2 = beam2
        beam2.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beam2.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beam2.createObject('MechanicalObject', position='0 0 1 0 0 0 1  1 0 1 0 0 0 1  2 0 1 0 0 0 1  3 0 1 0 0 0 1  4 0 1 0 0 0 1  5 0 1 0 0 0 1  6 0 1 0 0 0 1  7 0 1 0 0 0 1', name='DOFs', template='Rigid')
        beam2.createObject('Mesh', lines='0 1 1 2 2 3 3 4 4 5 5 6 6 7', name='lines')
        beam2.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beam2.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beam2.createObject('BeamFEMForceField', radius='0.1', name='FEM', poissonRatio='0.49', youngModulus='20000000')

        # rootNode/beam2/Collision
        Collision = beam2.createChild('Collision')
        self.Collision = Collision
        Collision.createObject('CubeTopology', nx='15', ny='2', nz='2', min='0 -0.1 -0.1', max='7 0.1 0.1')
        Collision.createObject('MechanicalObject')
        Collision.createObject('BeamLinearMapping', isMechanical='true')
        Collision.createObject('TriangleCollisionModel')

        # rootNode/beam3
        beam3 = rootNode.createChild('beam3')
        self.beam3 = beam3
        beam3.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beam3.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beam3.createObject('MechanicalObject', position='0 0 -1 0 0 0 1  1 0 -1 0 0 0 1  2 0 -1 0 0 0 1  3 0 -1 0 0 0 1  4 0 -1 0 0 0 1  5 0 -1 0 0 0 1  6 0 -1 0 0 0 1  7 0 -1 0 0 0 1', name='DOFs', template='Rigid')
        beam3.createObject('Mesh', lines='0 1 1 2 2 3 3 4 4 5 5 6 6 7', name='lines')
        beam3.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beam3.createObject('FixedConstraint', indices='7', name='FixedConstraint2')
        beam3.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beam3.createObject('BeamFEMForceField', radius='0.1', name='FEM', poissonRatio='0.49', youngModulus='20000000')

        # # rootNode/beam3/Collision33
        # Collision3 = beam3.createChild('Collision3')
        # self.Collision3 = Collision3
        # Collision3.createObject('CubeTopology', nx='15', ny='2', nz='2', min='0 -0.1 -0.1', max='7 0.1 0.1')
        # Collision3.createObject('MechanicalObject')
        # Collision3.createObject('BeamLinearMapping', isMechanical='true')
        # Collision3.createObject('TriangleCollisionModel')
        # rootNode/beam2/Collision
        Collision = beam3.createChild('Collision')
        self.Collision = Collision
        Collision.createObject('MechanicalObject')
        #Collision.createObject('SphereCollisionModel', position='0 0 0 0 0 0', radius='.2')
        Collision.createObject('SphereCollisionModel', radius='.2')
        Collision.createObject('RigidMapping', index='0 1 2')

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