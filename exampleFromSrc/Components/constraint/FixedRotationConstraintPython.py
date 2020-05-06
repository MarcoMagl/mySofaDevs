"""
FixedRotationConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/FixedRotationConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/FixedRotationConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class FixedRotationConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('VisualStyle', displayFlags='showVisual showBehaviorModels showForceFields showCollision showMapping')
        rootNode.createObject('DefaultPipeline', depth='6', verbose='0', draw='0', name='DefaultCollisionPipeline')
        rootNode.createObject('BruteForceDetection', name='Detection')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.2', alarmDistance='0.3', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='default')
        rootNode.createObject('DefaultCollisionGroupManager', name='Group')

        # rootNode/scene
        scene = rootNode.createChild('scene')
        self.scene = scene
        scene.gravity = '0 -9.81 0'
        scene.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        scene.createObject('CGLinearSolver', threshold='1e-09', tolerance='1e-12', name='linear solver', iterations='25', template='GraphScattered')

        # rootNode/scene/Rotation around Z axis not authorized
        Rotation_around_Z_axis_not_authorized = scene.createChild('Rotation around Z axis not authorized')
        self.Rotation_around_Z_axis_not_authorized = Rotation_around_Z_axis_not_authorized
        Rotation_around_Z_axis_not_authorized.gravity = '0 -9.81 0'
        Rotation_around_Z_axis_not_authorized.createObject('MechanicalObject', rotation='0 0 0', name='default0', template='Rigid3d', position='0 0 0 0 0 0 1 1 0 0 0 0 0 1', translation='0 0 0', restScale='1')
        Rotation_around_Z_axis_not_authorized.createObject('FixedConstraint', indices='0', name='default1', template='Rigid3d')
        Rotation_around_Z_axis_not_authorized.createObject('FixedRotationConstraint', FixedXRotation='0', FixedZRotation='1', name='default2', template='Rigid3d', FixedYRotation='0')
        Rotation_around_Z_axis_not_authorized.createObject('UniformMass', showAxisSizeFactor='1', name='default3', template='Rigid3d')

        # rootNode/scene/Rotation around Z axis not authorized/spring
        spring = Rotation_around_Z_axis_not_authorized.createChild('spring')
        self.spring = spring
        spring.gravity = '0 -9.81 0'
        spring.createObject('MechanicalObject', rotation='0 0 0', name='default4', template='Rigid3d', position='0 0 0 0 0 0 1 -1 0 0 0 0 0 1', translation='0 0 0', restScale='1')
        spring.createObject('UniformMass', showAxisSizeFactor='1', name='default54', template='Rigid3d')
        spring.createObject('RigidRigidMapping', axisLength='0.001', repartition='1 1', name='default1', template='Rigid3d,Rigid3d')
        spring.createObject('JointSpringForceField', spring='BEGIN_SPRING  0 1  KS_T 1e+06 100000  KS_R 0 1000  KS_B 100  END_SPRING
', name='default5', template='Rigid3d')

        # rootNode/scene/Rotation around Z axis is free
        Rotation_around_Z_axis_is_free = scene.createChild('Rotation around Z axis is free')
        self.Rotation_around_Z_axis_is_free = Rotation_around_Z_axis_is_free
        Rotation_around_Z_axis_is_free.gravity = '0 -9.81 0'
        Rotation_around_Z_axis_is_free.createObject('MechanicalObject', rotation='0 0 0', name='default6', template='Rigid3d', position='3 0 0 0 0 0 1 4 0 0 0 0 0 1', translation='0 0 0', restScale='1')
        Rotation_around_Z_axis_is_free.createObject('FixedConstraint', indices='0', name='default7', template='Rigid3d')
        Rotation_around_Z_axis_is_free.createObject('UniformMass', showAxisSizeFactor='1', name='default54', template='Rigid3d')

        # rootNode/scene/Rotation around Z axis is free/spring
        spring = Rotation_around_Z_axis_is_free.createChild('spring')
        self.spring = spring
        spring.gravity = '0 -9.81 0'
        spring.createObject('MechanicalObject', rotation='0 0 0', name='default9', template='Rigid3d', position='0 0 0 0 0 0 1 -1 0 0 0 0 0 1', translation='0 0 0', restScale='1')
        spring.createObject('UniformMass', showAxisSizeFactor='1', name='default10', template='Rigid3d')
        spring.createObject('RigidRigidMapping', axisLength='0.001', repartition='1 1', name='default11', template='Rigid3d,Rigid3d')
        spring.createObject('JointSpringForceField', spring='BEGIN_SPRING  0 1  END_SPRING
', name='default12', template='Rigid3d')

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
    rootNode.findData('dt').value = '0.02'
    rootNode.findData('gravity').value = '0 -9.81 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myFixedRotationConstraint = FixedRotationConstraint(rootNode,commandLineArguments)
    return 0;