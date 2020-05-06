"""
NonBuiltConstraintCorrectionPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/NonBuiltConstraintCorrection.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/NonBuiltConstraintCorrectionPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class NonBuiltConstraintCorrection (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showVisual showBehaviorModels')
        rootNode.createObject('FreeMotionAnimationLoop', build_lcp='false', maxIt='100', displayTime='1', initial_guess='true')
        rootNode.createObject('DefaultPipeline', draw='0', depth='8', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('LocalMinDistance', contactDistance='0.1', alarmDistance='0.35', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='FrictionContact')
        rootNode.createObject('LCPConstraintSolver', tolerance='0.001', maxIt='1000')

        # rootNode/unnamedNode_0
        unnamedNode_0 = rootNode.createChild('unnamedNode_0')
        self.unnamedNode_0 = unnamedNode_0
        unnamedNode_0.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        unnamedNode_0.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        unnamedNode_0.createObject('DefaultCollisionGroupManager', name='Group')

        # rootNode/unnamedNode_0/TORUS
        TORUS = unnamedNode_0.createChild('TORUS')
        self.TORUS = TORUS
        TORUS.createObject('MechanicalObject', scale='1.0', dz='0.0', template='Rigid3d', dx='0.0', dy='0.0')
        TORUS.createObject('UniformMass', printLog='false', totalMass='40.0')
        TORUS.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/TORUS/Visu
        Visu = TORUS.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='1.0', name='meshLoader_0', filename='mesh/torus.obj')
        Visu.createObject('OglModel', color='1.0 0.5 0.25 1.0', src='@meshLoader_0', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/TORUS/Surf2
        Surf2 = TORUS.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/torus_for_collision.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='1.0')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/MAN
        MAN = unnamedNode_0.createChild('MAN')
        self.MAN = MAN
        MAN.createObject('EulerExplicitSolver')
        MAN.createObject('MechanicalObject', dz='0.0', template='Rigid3d', dx='0.0', dy='0.0')
        MAN.createObject('UniformMass', printLog='false', totalMass='100.0')
        MAN.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/MAN/Visu
        Visu = MAN.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='10', name='meshLoader_2', filename='mesh/man.obj')
        Visu.createObject('OglModel', color='0.8 0.8 0.8 1.0', src='@meshLoader_2', name='Visual', dy='-3.0')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/MAN/Surf2
        Surf2 = MAN.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/man.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='10', dy='-3.0')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/CUBE
        CUBE = unnamedNode_0.createChild('CUBE')
        self.CUBE = CUBE
        CUBE.createObject('MechanicalObject', scale='0.3', dz='-0.5', template='Rigid3d', dx='-2.0', dy='-2.0')
        CUBE.createObject('UniformMass', printLog='false', totalMass='100.0')
        CUBE.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE/Visu
        Visu = CUBE.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_4', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.0 0.5 0.5 1.0', src='@meshLoader_4', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE/Surf2
        Surf2 = CUBE.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/DRAGON1
        DRAGON1 = unnamedNode_0.createChild('DRAGON1')
        self.DRAGON1 = DRAGON1
        DRAGON1.createObject('EulerExplicitSolver')
        DRAGON1.createObject('MechanicalObject', dz='2.5', template='Rigid3d', dx='0.0', dy='2.5')
        DRAGON1.createObject('UniformMass', printLog='false', totalMass='100.0')
        DRAGON1.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/DRAGON1/Visu
        Visu = DRAGON1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.25', name='meshLoader_1', filename='mesh/dragon_clean.obj')
        Visu.createObject('OglModel', color='0.2 0.2 0.8 1.0', src='@meshLoader_1', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/DRAGON1/Surf2
        Surf2 = DRAGON1.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/dragon_clean.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.25')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/BOX
        BOX = unnamedNode_0.createChild('BOX')
        self.BOX = BOX
        BOX.createObject('MeshObjLoader', filename='mesh/box_inside.obj', triangulate='true', name='loader')
        BOX.createObject('MeshTopology', src='@loader')
        BOX.createObject('MechanicalObject', src='@loader')
        BOX.createObject('TriangleCollisionModel', moving='0', simulated='0')
        BOX.createObject('LineCollisionModel', moving='0', simulated='0')
        BOX.createObject('PointCollisionModel', moving='0', simulated='0')
        BOX.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_3', filename='mesh/box_outside.obj')
        BOX.createObject('OglModel', color='1 0 0 0.3', src='@meshLoader_3', name='Visual')

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
    rootNode.findData('dt').value = '0.03'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myNonBuiltConstraintCorrection = NonBuiltConstraintCorrection(rootNode,commandLineArguments)
    return 0;