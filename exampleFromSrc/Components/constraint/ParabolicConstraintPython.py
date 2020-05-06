"""
ParabolicConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/ParabolicConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/ParabolicConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class ParabolicConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showVisual showBehaviorModels')
        rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('NewProximityIntersection', contactDistance='0.2', alarmDistance='0.3', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='default')
        rootNode.createObject('DefaultCollisionGroupManager', name='Group')

        # rootNode/LiverParabolic
        LiverParabolic = rootNode.createChild('LiverParabolic')
        self.LiverParabolic = LiverParabolic
        LiverParabolic.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        LiverParabolic.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        LiverParabolic.createObject('MechanicalObject', position='0 0 0 0 0 0 1', name='DOFs', template='Rigid3d')
        LiverParabolic.createObject('UniformMass', showAxisSizeFactor='0.1', name='mass', totalMass='1')
        LiverParabolic.createObject('ParabolicConstraint', P2='5 3 1', P3='7 6 -5', P1='1 0 0', name='parabol', indices='0', EndTime='1.5', BeginTime='0.5')

        # rootNode/LiverParabolic/Visu
        Visu = LiverParabolic.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_1', filename='mesh/liver-smooth.obj')
        Visu.createObject('OglModel', color='red', src='@meshLoader_1', name='VisualModel')
        Visu.createObject('RigidMapping', input='@..', name='visual mapping', output='@VisualModel')

        # rootNode/LiverParabolic/Surf
        Surf = LiverParabolic.createChild('Surf')
        self.Surf = Surf
        Surf.createObject('SphereLoader', filename='mesh/liver.sph')
        Surf.createObject('MechanicalObject', position='@[-1].position')
        Surf.createObject('SphereCollisionModel', listRadius='@[-2].listRadius', name='CollisionModel')
        Surf.createObject('RigidMapping', name='sphere mapping')

        # rootNode/CubeFixed
        CubeFixed = rootNode.createChild('CubeFixed')
        self.CubeFixed = CubeFixed
        CubeFixed.createObject('MeshObjLoader', name='loader', filename='mesh/cube.obj')
        CubeFixed.createObject('MeshTopology', src='@loader')
        CubeFixed.createObject('MechanicalObject', src='@loader', scale='20', dz='-35')
        CubeFixed.createObject('TriangleCollisionModel', moving='0', simulated='0')
        CubeFixed.createObject('MeshObjLoader', handleSeams='1', scale='20', name='meshLoader_0', filename='mesh/cube.obj')
        CubeFixed.createObject('OglModel', color='gray', src='@meshLoader_0', dz='-35', name='Visual')

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
    rootNode.findData('dt').value = '0.01'
    rootNode.findData('multiThreadSimulation').value = '0'
    rootNode.findData('time').value = '0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myParabolicConstraint = ParabolicConstraint(rootNode,commandLineArguments)
    return 0;