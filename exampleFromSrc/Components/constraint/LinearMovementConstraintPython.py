"""
LinearMovementConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/LinearMovementConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/LinearMovementConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class LinearMovementConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')

        # rootNode/Spoon1
        Spoon1 = rootNode.createChild('Spoon1')
        self.Spoon1 = Spoon1
        Spoon1.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        Spoon1.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        Spoon1.createObject('MechanicalObject', dz='0', name='default118', dx='0', dy='0', position='0 1.41421 0 0 0 0.382683 0.92388', rest_position='0 1.41421 0 0 0 0.382683 0.92388', template='Rigid3d')
        keyTimes = '0 2 10 40 50' 
        movements = '0 0 0   0 0 0                 0 0 0   0 0 0                 0 0 -1  0 0 0                 0 0 -1  0 0 6.3                 0 0 -1   0 0 6.3'
        Spoon1.createObject('LinearMovementConstraint', keyTimes=keyTimes, template='Rigid3d', movements=movements)

        # rootNode/Spoon1/coli
        coli = Spoon1.createChild('coli')
        self.coli = coli
        coli.createObject('MeshObjLoader', name='loader', filename='mesh/liver.obj')
        coli.createObject('MeshTopology', src='@loader')
        coli.createObject('MechanicalObject', src='@loader', name='dofs', template='Vec3d')
        coli.createObject('TriangleCollisionModel', contactStiffness='100000000', moving='1', simulated='1')
        coli.createObject('RigidMapping', template='Rigid3d,Vec3d')

        # rootNode/Spoon1/Visu
        Visu = Spoon1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_1', filename='mesh/liver.obj')
        Visu.createObject('OglModel', color='red', src='@meshLoader_1', name='Visual')
        Visu.createObject('RigidMapping', input='@..', name='default161', template='Rigid3d,ExtVec3f', output='@Visual')

        # rootNode/Spoon2
        Spoon2 = rootNode.createChild('Spoon2')
        self.Spoon2 = Spoon2
        Spoon2.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        Spoon2.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        Spoon2.createObject('MechanicalObject', dz='0', name='default118', dx='10', dy='0', position='0 1.41421 0 0 0 0.382683 0.92388', rest_position='0 1.41421 0 0 0 0.382683 0.92388', template='Rigid3d')
        Spoon2.createObject('LinearMovementConstraint', keyTimes='0 2 10 40 50', template='Rigid3d', movements='0 0 0   0 0 0                 0 0 0   0 0 0                 0 0 -1  0 0 0                 0 0 -1  0 0 6.3                 0 0 0   0 0 6.3')

        # rootNode/Spoon2/coli
        coli = Spoon2.createChild('coli')
        self.coli = coli
        coli.createObject('MeshObjLoader', name='loader', filename='mesh/liver.obj')
        coli.createObject('MeshTopology', src='@loader')
        coli.createObject('MechanicalObject', src='@loader', name='dofs', template='Vec3d')
        coli.createObject('TriangleCollisionModel', contactStiffness='100000000', moving='1', simulated='1')
        coli.createObject('RigidMapping', template='Rigid3d,Vec3d')

        # rootNode/Spoon2/Visu
        Visu = Spoon2.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_0', filename='mesh/liver.obj')
        Visu.createObject('OglModel', color='green', src='@meshLoader_0', name='Visual')
        Visu.createObject('RigidMapping', input='@..', name='default161', template='Rigid3d,ExtVec3f', output='@Visual')

        # rootNode/Spoon3
        Spoon3 = rootNode.createChild('Spoon3')
        self.Spoon3 = Spoon3
        Spoon3.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        Spoon3.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        Spoon3.createObject('MechanicalObject', dz='0', name='default118', dx='20', dy='0', position='0 1.41421 0 0 0 0.382683 0.92388', rest_position='0 1.41421 0 0 0 0.382683 0.92388', template='Rigid3d')
        Spoon3.createObject('LinearMovementConstraint', keyTimes='0 2 10 40 50', template='Rigid3d', movements='0 0 0   0 0 0                 0 0 0   0 0 0                 0 0 -1  0 0 0                 0 0 -1  0 0 6.3                 0 0 -1   0 0 0')

        # rootNode/Spoon3/coli
        coli = Spoon3.createChild('coli')
        self.coli = coli
        coli.createObject('MeshObjLoader', name='loader', filename='mesh/liver.obj')
        coli.createObject('MeshTopology', src='@loader')
        coli.createObject('MechanicalObject', src='@loader', name='dofs', template='Vec3d')
        coli.createObject('TriangleCollisionModel', contactStiffness='100000000', moving='1', simulated='1')
        coli.createObject('RigidMapping', template='Rigid3d,Vec3d')

        # rootNode/Spoon3/Visu
        Visu = Spoon3.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_2', filename='mesh/liver.obj')
        Visu.createObject('OglModel', color='blue', src='@meshLoader_2', name='Visual')
        Visu.createObject('RigidMapping', input='@..', name='default161', template='Rigid3d,ExtVec3f', output='@Visual')

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
    rootNode.findData('dt').value = '0.1'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myLinearMovementConstraint = LinearMovementConstraint(rootNode,commandLineArguments)
    return 0;