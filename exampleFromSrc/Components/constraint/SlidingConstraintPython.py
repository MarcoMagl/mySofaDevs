"""
SlidingConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/SlidingConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/SlidingConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class SlidingConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showForceFields showVisual showBehavior')
        rootNode.createObject('FreeMotionAnimationLoop')
        rootNode.createObject('GenericConstraintSolver', maxIterations='1000', tolerance='0.001')
        rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('LocalMinDistance', contactDistance='0.09', alarmDistance='0.2', name='Proximity', angleCone='0.0')
        rootNode.createObject('DefaultContactManager', name='Response', response='FrictionContact')
        rootNode.createObject('DefaultCollisionGroupManager', name='Group')

        # rootNode/SlidingPoint
        SlidingPoint = rootNode.createChild('SlidingPoint')
        self.SlidingPoint = SlidingPoint
        SlidingPoint.createObject('MechanicalObject', position='1 1.25 -0.2 	1 1.25 0.2', name='points', template='Vec3d', free_position='1 1.25 -0.2 	1 1.25 0.2')

        # rootNode/CUBE_1
        CUBE_1 = rootNode.createChild('CUBE_1')
        self.CUBE_1 = CUBE_1
        CUBE_1.createObject('EulerImplicitSolver', rayleighStiffness='0.1', printLog='false', rayleighMass='0.1')
        CUBE_1.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', iterations='25')
        CUBE_1.createObject('MechanicalObject', scale='1.0', dz='0.0', template='Rigid3d', dx='0.0', dy='0')
        CUBE_1.createObject('UniformMass', totalMass='10.0')
        CUBE_1.createObject('UncoupledConstraintCorrection')

        # rootNode/CUBE_1/Visu
        Visu = CUBE_1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('OglModel', color='1 1 0 1.0', name='Visual', filename='mesh/cube.obj')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/CUBE_1/ColliCube
        ColliCube = CUBE_1.createChild('ColliCube')
        self.ColliCube = ColliCube
        ColliCube.createObject('MeshTopology', filename='mesh/cube.obj')
        ColliCube.createObject('MechanicalObject', scale='1.0')
        ColliCube.createObject('TriangleCollisionModel', contactStiffness='0.1')
        ColliCube.createObject('LineCollisionModel', contactStiffness='0.1')
        ColliCube.createObject('PointCollisionModel', contactStiffness='0.1')
        ColliCube.createObject('RigidMapping')

        # rootNode/CUBE_1/Constraints
        Constraints = CUBE_1.createChild('Constraints')
        self.Constraints = Constraints
        Constraints.createObject('MechanicalObject', position='1 1.25 1	1 1.25 -1	0 0 0', name='points', template='Vec3d')
        Constraints.createObject('RigidMapping')
        rootNode.createObject('SlidingConstraint', object1='@SlidingPoint/points', object2='@CUBE_1/Constraints/points', sliding_point='0', name='constraint1', axis_1='0', axis_2='1')

        # rootNode/Line
        Line = rootNode.createChild('Line')
        self.Line = Line
        Line.createObject('MechanicalObject', position='6 1.25 1	6 1.25 -1', name='points', template='Vec3d', free_position='6 1.25 1	6 1.25 -1')

        # # rootNode/CUBE_2
        # CUBE_2 = rootNode.createChild('CUBE_2')
        # self.CUBE_2 = CUBE_2
        # CUBE_2.createObject('EulerImplicitSolver', printLog='false')
        # CUBE_2.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', iterations='25')
        # CUBE_2.createObject('MechanicalObject', scale='1.0', dz='0.0', template='Rigid3d', dx='5.0', dy='0')
        # CUBE_2.createObject('UniformMass', totalMass='10.0')
        # CUBE_2.createObject('UncoupledConstraintCorrection')

        # # rootNode/CUBE_2/Visu
        # Visu = CUBE_2.createChild('Visu')
        # self.Visu = Visu
        # Visu.createObject('OglModel', color='1 1 0 1.0', name='Visual', filename='mesh/cube.obj')
        # Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # # rootNode/CUBE_2/ColliCube
        # ColliCube = CUBE_2.createChild('ColliCube')
        # self.ColliCube = ColliCube
        # ColliCube.createObject('MeshTopology', filename='mesh/cube.obj')
        # ColliCube.createObject('MechanicalObject', scale='1.0')
        # ColliCube.createObject('TriangleCollisionModel', contactStiffness='0.1')
        # ColliCube.createObject('LineCollisionModel', contactStiffness='0.1')
        # ColliCube.createObject('PointCollisionModel', contactStiffness='0.1')
        # ColliCube.createObject('RigidMapping')

        # # rootNode/CUBE_2/Constraints
        # Constraints = CUBE_2.createChild('Constraints')
        # self.Constraints = Constraints
        # Constraints.createObject('MechanicalObject', position='1 1.25 1', name='points', template='Vec3d')
        # Constraints.createObject('RigidMapping')
        # rootNode.createObject('SlidingConstraint', object1='@CUBE_2/Constraints/points', object2='@Line/points', sliding_point='0', name='constraint2', axis_1='0', axis_2='1')

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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = '0.001'
    rootNode.findData('gravity').value = '0 -9.81 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    mySlidingConstraint = SlidingConstraint(rootNode,commandLineArguments)
    return 0;