"""
FrictionContact_VelocityConstraintsPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/FrictionContact_VelocityConstraints.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/FrictionContact_VelocityConstraintsPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class FrictionContact_VelocityConstraints (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showVisual')
        rootNode.createObject('GenericConstraintSolver', maxIterations='1000', tolerance='1e-6')
        rootNode.createObject('FreeMotionAnimationLoop', solveVelocityConstraintFirst='1')
        rootNode.createObject('DefaultPipeline', draw='0', depth='15', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('LocalMinDistance', useLMDFilters='0', contactDistance='0.1', alarmDistance='0.3', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='FrictionContact')

        # rootNode/unnamedNode_0
        unnamedNode_0 = rootNode.createChild('unnamedNode_0')
        self.unnamedNode_0 = unnamedNode_0
        unnamedNode_0.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        unnamedNode_0.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        unnamedNode_0.createObject('DefaultCollisionGroupManager', name='Group')

        # rootNode/unnamedNode_0/CUBE_1_1
        CUBE_1_1 = unnamedNode_0.createChild('CUBE_1_1')
        self.CUBE_1_1 = CUBE_1_1
        CUBE_1_1.createObject('MechanicalObject', scale='0.3', dz='0.0', dx='-2.8', template='Rigid3d', dy='-1.5', rx='0')
        CUBE_1_1.createObject('UniformMass', totalMass='100.0')
        CUBE_1_1.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE_1_1/Visu
        Visu = CUBE_1_1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_4', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.0 0.5 0.8 1.0', src='@meshLoader_4', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE_1_1/Surf2
        Surf2 = CUBE_1_1.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/CUBE_1_2
        CUBE_1_2 = unnamedNode_0.createChild('CUBE_1_2')
        self.CUBE_1_2 = CUBE_1_2
        CUBE_1_2.createObject('MechanicalObject', scale='0.3', dz='0.0', dx='0.0', template='Rigid3d', dy='-1.5', ry='0')
        CUBE_1_2.createObject('UniformMass', totalMass='100.0')
        CUBE_1_2.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE_1_2/Visu
        Visu = CUBE_1_2.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_1', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.0 0.9 0.8 1.0', src='@meshLoader_1', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE_1_2/Surf2
        Surf2 = CUBE_1_2.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/CUBE_1_3
        CUBE_1_3 = unnamedNode_0.createChild('CUBE_1_3')
        self.CUBE_1_3 = CUBE_1_3
        CUBE_1_3.createObject('MechanicalObject', scale='0.3', dz='0.0', dx='2.8', template='Rigid3d', dy='-1.5', rx='0')
        CUBE_1_3.createObject('UniformMass', totalMass='100.0')
        CUBE_1_3.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE_1_3/Visu
        Visu = CUBE_1_3.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_5', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.0 0.5 0.8 1.0', src='@meshLoader_5', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE_1_3/Surf2
        Surf2 = CUBE_1_3.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/CUBE_2_1
        CUBE_2_1 = unnamedNode_0.createChild('CUBE_2_1')
        self.CUBE_2_1 = CUBE_2_1
        CUBE_2_1.createObject('MechanicalObject', scale='0.3', dz='0.0', dx='-1.5', template='Rigid3d', dy='1', rz='45')
        CUBE_2_1.createObject('UniformMass', totalMass='100.0')
        CUBE_2_1.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE_2_1/Visu
        Visu = CUBE_2_1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_2', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.5 0.0 0.5 1.0', src='@meshLoader_2', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE_2_1/Surf2
        Surf2 = CUBE_2_1.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/CUBE_2_2
        CUBE_2_2 = unnamedNode_0.createChild('CUBE_2_2')
        self.CUBE_2_2 = CUBE_2_2
        CUBE_2_2.createObject('MechanicalObject', scale='0.3', dz='0.0', dx='1.5', template='Rigid3d', dy='1', rz='45')
        CUBE_2_2.createObject('UniformMass', totalMass='100.0')
        CUBE_2_2.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE_2_2/Visu
        Visu = CUBE_2_2.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_6', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.5 0.0 0.5 1.0', src='@meshLoader_6', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE_2_2/Surf2
        Surf2 = CUBE_2_2.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
        Surf2.createObject('TriangleCollisionModel')
        Surf2.createObject('LineCollisionModel')
        Surf2.createObject('PointCollisionModel')
        Surf2.createObject('RigidMapping')

        # rootNode/unnamedNode_0/CUBE_3_1
        CUBE_3_1 = unnamedNode_0.createChild('CUBE_3_1')
        self.CUBE_3_1 = CUBE_3_1
        CUBE_3_1.createObject('MechanicalObject', scale='0.3', dz='0.0', dx='0.0', template='Rigid3d', dy='3.5', rx='0')
        CUBE_3_1.createObject('UniformMass', totalMass='100.0')
        CUBE_3_1.createObject('UncoupledConstraintCorrection')

        # rootNode/unnamedNode_0/CUBE_3_1/Visu
        Visu = CUBE_3_1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_3', filename='mesh/smCube27.obj')
        Visu.createObject('OglModel', color='0.9 0.0 0.2 1.0', src='@meshLoader_3', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

        # rootNode/unnamedNode_0/CUBE_3_1/Surf2
        Surf2 = CUBE_3_1.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.createObject('MeshObjLoader', filename='mesh/smCube27.obj', triangulate='true', name='loader')
        Surf2.createObject('MeshTopology', src='@loader')
        Surf2.createObject('MechanicalObject', src='@loader', scale='0.3')
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
        BOX.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_0', filename='mesh/box_outside.obj')
        BOX.createObject('OglModel', color='0 0.8 0.3 0.3', src='@meshLoader_0', name='Visual')

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
    rootNode.findData('gravity').value = '0 -9.810 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myFrictionContact_VelocityConstraints = FrictionContact_VelocityConstraints(rootNode,commandLineArguments)
    return 0;