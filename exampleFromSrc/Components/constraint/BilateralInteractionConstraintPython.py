"""
BilateralInteractionConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/BilateralInteractionConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/BilateralInteractionConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class BilateralInteractionConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaMiscCollision')
        rootNode.createObject('VisualStyle', displayFlags='showForceFields')
        rootNode.createObject('FreeMotionAnimationLoop')
        rootNode.createObject('GenericConstraintSolver', maxIterations='1000', tolerance='0.001')
        rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('LocalMinDistance', contactDistance='0.09', alarmDistance='0.2', name='Proximity', angleCone='0.0')
        rootNode.createObject('DefaultContactManager', name='Response', response='FrictionContact')
        rootNode.createObject('DefaultCollisionGroupManager', name='Group')

        # rootNode/CUBE_0
        CUBE_0 = rootNode.createChild('CUBE_0')
        self.CUBE_0 = CUBE_0
        CUBE_0.createObject('MechanicalObject', dy='2.5')

        # rootNode/CUBE_0/Visu
        Visu = CUBE_0.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_0', filename='mesh/cube.obj')
        Visu.createObject('OglModel', color='1 0 0 1', src='@meshLoader_0', name='Visual', dy='2.5')

        # rootNode/CUBE_0/ColliCube
        ColliCube = CUBE_0.createChild('ColliCube')
        self.ColliCube = ColliCube
        ColliCube.createObject('MeshObjLoader', filename='mesh/cube.obj', triangulate='1', name='loader')
        ColliCube.createObject('MeshTopology', src='@loader')
        ColliCube.createObject('MechanicalObject', src='@loader', template='Vec3d', dy='2.5')
        ColliCube.createObject('TriangleCollisionModel', moving='0', simulated='0')
        ColliCube.createObject('LineCollisionModel', moving='0', simulated='0')
        ColliCube.createObject('PointCollisionModel', moving='0', simulated='0')

        # rootNode/CUBE_0/Constraints
        Constraints = CUBE_0.createChild('Constraints')
        self.Constraints = Constraints
        Constraints.createObject('MechanicalObject', position='1 1.25 1', name='points', template='Vec3d')

        # rootNode/CUBE_1
        CUBE_1 = rootNode.createChild('CUBE_1')
        self.CUBE_1 = CUBE_1
        CUBE_1.createObject('EulerImplicitSolver', rayleighStiffness='0.1', printLog='false', rayleighMass='0.1')
        CUBE_1.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', iterations='25')
        CUBE_1.createObject('MechanicalObject', scale='1.0', dz='0.0', template='Rigid3d', dx='0.0', dy='0')
        CUBE_1.createObject('UniformMass', totalMass='0.1')
        CUBE_1.createObject('UncoupledConstraintCorrection')

        # rootNode/CUBE_1/Visu
        Visu = CUBE_1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_2', filename='mesh/cube.obj')
        Visu.createObject('OglModel', color='1 1 0 1.0', src='@meshLoader_2', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/CUBE_1/ColliCube
        ColliCube = CUBE_1.createChild('ColliCube')
        self.ColliCube = ColliCube
        ColliCube.createObject('MeshObjLoader', filename='mesh/cube.obj', triangulate='1', name='loader')
        ColliCube.createObject('MeshTopology', src='@loader')
        ColliCube.createObject('MechanicalObject', src='@loader')
        ColliCube.createObject('TriangleCollisionModel', contactStiffness='10.0')
        ColliCube.createObject('LineCollisionModel', contactStiffness='10.0')
        ColliCube.createObject('PointCollisionModel', contactStiffness='10.0')
        ColliCube.createObject('RigidMapping')

        # rootNode/CUBE_1/Constraints
        Constraints = CUBE_1.createChild('Constraints')
        self.Constraints = Constraints
        Constraints.createObject('MechanicalObject', position='1 1.25 1	-1.25 -1.25 1.25', name='points', template='Vec3d')
        Constraints.createObject('RigidMapping')
        rootNode.createObject('BilateralInteractionConstraint', object1='@CUBE_0/Constraints/points', object2='@CUBE_1/Constraints/points', second_point='0', first_point='0', template='Vec3d')

        # rootNode/CUBE_2
        CUBE_2 = rootNode.createChild('CUBE_2')
        self.CUBE_2 = CUBE_2
        CUBE_2.createObject('EulerImplicitSolver', rayleighStiffness='0.1', printLog='false', rayleighMass='0.1')
        CUBE_2.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', iterations='25')
        CUBE_2.createObject('MechanicalObject', scale='1.0', dz='0.0', template='Rigid3d', dx='0.0', dy='-2.5')
        CUBE_2.createObject('UniformMass', totalMass='0.1')
        CUBE_2.createObject('UncoupledConstraintCorrection')

        # rootNode/CUBE_2/Visu
        Visu = CUBE_2.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_3', filename='mesh/cube.obj')
        Visu.createObject('OglModel', color='0 1 0 1.0', src='@meshLoader_3', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/CUBE_2/ColliCube
        ColliCube = CUBE_2.createChild('ColliCube')
        self.ColliCube = ColliCube
        ColliCube.createObject('MeshObjLoader', name='loader', filename='mesh/cube.obj')
        ColliCube.createObject('MeshTopology', src='@loader')
        ColliCube.createObject('MechanicalObject', src='@loader', scale='1.0')
        ColliCube.createObject('TriangleCollisionModel')
        ColliCube.createObject('LineCollisionModel')
        ColliCube.createObject('PointCollisionModel')
        ColliCube.createObject('RigidMapping')

        # rootNode/CUBE_2/Constraints
        Constraints = CUBE_2.createChild('Constraints')
        self.Constraints = Constraints
        Constraints.createObject('MechanicalObject', position='-1.25 1.25 1.25	1.25 -1.25 -1.25', name='points', template='Vec3d')
        Constraints.createObject('RigidMapping')
        rootNode.createObject('BilateralInteractionConstraint', object1='@CUBE_1/Constraints/points', object2='@CUBE_2/Constraints/points', second_point='0', first_point='1', template='Vec3d')

        # rootNode/CUBE_3
        CUBE_3 = rootNode.createChild('CUBE_3')
        self.CUBE_3 = CUBE_3
        CUBE_3.createObject('EulerImplicitSolver', rayleighStiffness='0.1', printLog='false', rayleighMass='0.1')
        CUBE_3.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', iterations='25')
        CUBE_3.createObject('MechanicalObject', scale='1.0', dz='0.0', template='Rigid3d', dx='0.0', dy='-5.0')
        CUBE_3.createObject('UniformMass', totalMass='0.1')
        CUBE_3.createObject('UncoupledConstraintCorrection')

        # rootNode/CUBE_3/Visu
        Visu = CUBE_3.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_4', filename='mesh/cube.obj')
        Visu.createObject('OglModel', color='0 1 1 1.0', src='@meshLoader_4', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/CUBE_3/ColliCube
        ColliCube = CUBE_3.createChild('ColliCube')
        self.ColliCube = ColliCube
        ColliCube.createObject('MeshObjLoader', name='loader', filename='mesh/cube.obj')
        ColliCube.createObject('MeshTopology', src='@loader')
        ColliCube.createObject('MechanicalObject', src='@loader', scale='1.0')
        ColliCube.createObject('TriangleCollisionModel')
        ColliCube.createObject('LineCollisionModel')
        ColliCube.createObject('PointCollisionModel')
        ColliCube.createObject('RigidMapping')

        # rootNode/CUBE_3/Constraints
        Constraints = CUBE_3.createChild('Constraints')
        self.Constraints = Constraints
        Constraints.createObject('MechanicalObject', position='1.25 1.25 -1.25', name='points', template='Vec3d')
        Constraints.createObject('RigidMapping')
        rootNode.createObject('BilateralInteractionConstraint', object1='@CUBE_2/Constraints/points', object2='@CUBE_3/Constraints/points', second_point='0', first_point='1', template='Vec3d')

        # rootNode/CUBE_4
        CUBE_4 = rootNode.createChild('CUBE_4')
        self.CUBE_4 = CUBE_4
        CUBE_4.createObject('EulerImplicitSolver', rayleighStiffness='0.1', printLog='false', rayleighMass='0.1')
        CUBE_4.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', iterations='25')
        CUBE_4.createObject('MechanicalObject', scale='1.0', dz='-2.5', template='Rigid3d', dx='0.0', dy='-2.5')
        CUBE_4.createObject('UniformMass', totalMass='0.1')
        CUBE_4.createObject('UncoupledConstraintCorrection')

        # rootNode/CUBE_4/Visu
        Visu = CUBE_4.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_1', filename='mesh/cube.obj')
        Visu.createObject('OglModel', color='0 0 1 1.0', src='@meshLoader_1', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/CUBE_4/ColliCube
        ColliCube = CUBE_4.createChild('ColliCube')
        self.ColliCube = ColliCube
        ColliCube.createObject('MeshObjLoader', name='loader', filename='mesh/cube.obj')
        ColliCube.createObject('MeshTopology', src='@loader')
        ColliCube.createObject('MechanicalObject', src='@loader', scale='1.0')
        ColliCube.createObject('TriangleCollisionModel')
        ColliCube.createObject('LineCollisionModel')
        ColliCube.createObject('PointCollisionModel')
        ColliCube.createObject('RigidMapping')

        # rootNode/CUBE_4/Constraints
        Constraints = CUBE_4.createChild('Constraints')
        self.Constraints = Constraints
        Constraints.createObject('MechanicalObject', position='1.25 -1.25 1.25	1.25 1.25 1.25', name='points', template='Vec3d')
        Constraints.createObject('RigidMapping')
        rootNode.createObject('BilateralInteractionConstraint', object1='@CUBE_2/Constraints/points', object2='@CUBE_4/Constraints/points', second_point='0', first_point='1', template='Vec3d')

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
    rootNode.findData('gravity').value = '0 -981 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myBilateralInteractionConstraint = BilateralInteractionConstraint(rootNode,commandLineArguments)
    return 0;