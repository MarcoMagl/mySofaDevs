"""
LMConstraintCollisionResponsePython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/LMConstraintCollisionResponse.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/LMConstraintCollisionResponsePython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class LMConstraintCollisionResponse (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showCollisionModels')
        rootNode.createObject('DefaultPipeline')
        rootNode.createObject('BruteForceDetection')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.1', alarmDistance='0.3', name='Proximity')
        rootNode.createObject('DefaultContactManager', response='distanceLMConstraint')
        rootNode.createObject('DefaultCollisionGroupManager')

        # rootNode/Rigid
        Rigid = rootNode.createChild('Rigid')
        self.Rigid = Rigid
        Rigid.createObject('EulerImplicitSolver', rayleighStiffness='0.1', rayleighMass='0.1')
        Rigid.createObject('LMConstraintSolver', maxError='1e-7', numIterations='27')
        Rigid.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', iterations='25')
        Rigid.createObject('MechanicalObject', translation='0 3 0', template='Rigid3d')
        Rigid.createObject('UniformMass', totalMass='4')

        # rootNode/Rigid/Collision
        Collision = Rigid.createChild('Collision')
        self.Collision = Collision
        Collision.createObject('MeshObjLoader', name='loader', filename='mesh/cube.obj')
        Collision.createObject('MeshTopology', src='@loader')
        Collision.createObject('MechanicalObject')
        Collision.createObject('TriangleCollisionModel', contactStiffness='100', contactFriction='1')
        Collision.createObject('LineCollisionModel', contactStiffness='@[-1].contactStiffness', contactFriction='@[-1].contactFriction')
        Collision.createObject('PointCollisionModel', contactStiffness='@[-1].contactStiffness', contactFriction='@[-1].contactFriction')
        Collision.createObject('RigidMapping', input='@..', output='@.')

        # rootNode/FEM
        FEM = rootNode.createChild('FEM')
        self.FEM = FEM
        FEM.createObject('EulerImplicitSolver')
        FEM.createObject('LMConstraintSolver', maxError='1e-7', numIterations='27')
        FEM.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', iterations='25')
        FEM.createObject('SparseGridTopology', fileTopology='mesh/sphere.obj', n='4 4 4')
        FEM.createObject('MechanicalObject', translation='0 6 0', name='INDE1')
        FEM.createObject('UniformMass', separateGravity='0', totalMass='4')
        FEM.createObject('TetrahedronFEMForceField', poissonRatio='0.45', youngModulus='1000')

        # rootNode/FEM/CollisionNode
        CollisionNode = FEM.createChild('CollisionNode')
        self.CollisionNode = CollisionNode
        CollisionNode.createObject('MeshObjLoader', name='loader', filename='mesh/sphere.obj')
        CollisionNode.createObject('MeshTopology', src='@loader')
        CollisionNode.createObject('MechanicalObject')
        CollisionNode.createObject('TriangleCollisionModel', contactStiffness='10', contactFriction='1')
        CollisionNode.createObject('LineCollisionModel', contactStiffness='@[-1].contactStiffness', contactFriction='@[-1].contactFriction')
        CollisionNode.createObject('PointCollisionModel', contactStiffness='@[-1].contactStiffness', contactFriction='@[-1].contactFriction')
        CollisionNode.createObject('BarycentricMapping', input='@..', output='@.')

        # rootNode/Floor
        Floor = rootNode.createChild('Floor')
        self.Floor = Floor

        # rootNode/Floor/BaseGround-Friction0.5
        BaseGround_Friction0_5 = Floor.createChild('BaseGround-Friction0.5')
        self.BaseGround_Friction0_5 = BaseGround_Friction0_5
        BaseGround_Friction0_5.createObject('MeshObjLoader', name='loader', filename='mesh/cube.obj')
        BaseGround_Friction0_5.createObject('MeshTopology', src='@loader')
        BaseGround_Friction0_5.createObject('MechanicalObject', scale3d='12 1 12', src='@loader', translation='0 -6 0')
        BaseGround_Friction0_5.createObject('TriangleCollisionModel', moving='0', contactFriction='0.5', simulated='0')
        BaseGround_Friction0_5.createObject('LineCollisionModel', moving='0', contactFriction='@[-1].contactFriction', simulated='0')
        BaseGround_Friction0_5.createObject('PointCollisionModel', moving='0', contactFriction='@[-1].contactFriction', simulated='0')

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
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myLMConstraintCollisionResponse = LMConstraintCollisionResponse(rootNode,commandLineArguments)
    return 0;