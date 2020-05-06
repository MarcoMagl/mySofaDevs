"""
DistanceLMContactConstraint_DirectSolverPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/DistanceLMContactConstraint_DirectSolver.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/DistanceLMContactConstraint_DirectSolverPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class DistanceLMContactConstraint_DirectSolver (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')
        rootNode.createObject('DefaultPipeline', draw='0', name='default0', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.7', alarmDistance='0.8', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='distanceLMConstraint')
        rootNode.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        rootNode.createObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='25', template='GraphScattered')
        rootNode.createObject('LMConstraintDirectSolver', maxError='1e-7', constraintPos='0', constraintVel='1', name='default0', listening='1', numIterations='1', solverAlgorithm='SVD')

        # rootNode/cubeFEM
        cubeFEM = rootNode.createChild('cubeFEM')
        self.cubeFEM = cubeFEM
        cubeFEM.gravity = '0 -9.81 0'
        cubeFEM.createObject('MechanicalObject', force='0 0 0', name='dof', free_position='0 0 0', restScale='1', free_velocity='0 0 0', template='Vec3d', position='0 0 0', velocity='0 0 0', translation='0 2 0', rotation='30 20 15', derivX='0 0 0')
        cubeFEM.createObject('UniformMass', vertexMass='0.25', name='default2', template='Vec3d')
        cubeFEM.createObject('RegularGridTopology', max='3.5 3.5 3.5', p0='-3.5 -3.5 -3.5', n='5 5 5', name='default3', min='-3.5 -3.5 -3.5')
        cubeFEM.createObject('TetrahedronFEMForceField', poissonRatio='0.3', name='FEM', computeGlobalMatrix='0', updateStiffnessMatrix='0', method='large', template='Vec3d', youngModulus='25')

        # rootNode/cubeFEM/Visu
        Visu = cubeFEM.createChild('Visu')
        self.Visu = Visu
        Visu.gravity = '0 -9.81 0'
        Visu.createObject('MeshObjLoader', scale3d='@../dof.scale3d', name='meshLoader_0', handleSeams='1', translation='@../dof.translation', rotation='@../dof.rotation', filename='mesh/smCube125.obj')
        Visu.createObject('OglModel', src='@meshLoader_0', material='Default Diffuse 1 1 0 0 1 Ambient 1 0.2 0 0 1 Specular 0 1 0 0 1 Emissive 0 1 0 0 1 Shininess 0 45', name='Visual', template='ExtVec3f')
        Visu.createObject('SubsetMapping', input='@..', name='default4', template='Vec3d,ExtVec3f', output='@Visual')

        # rootNode/cubeFEM/Surf
        Surf = cubeFEM.createChild('Surf')
        self.Surf = Surf
        Surf.gravity = '0 -9.81 0'
        Surf.createObject('MeshObjLoader', name='loader', filename='mesh/smCube125.obj')
        Surf.createObject('MeshTopology', src='@loader', name='default5')
        Surf.createObject('MechanicalObject', scale3d='@../dof.scale3d', src='@loader', force='0 0 0', name='default6', free_position='0 0 0', restScale='1', free_velocity='0 0 0', template='Vec3d', velocity='0 0 0', position='0 0 0', translation='@../dof.translation', rotation='@../dof.rotation', derivX='0 0 0')
        Surf.createObject('TriangleCollisionModel', name='default1', template='Vec3d', contactFriction='0.6')
        Surf.createObject('LineCollisionModel', name='default2', contactFriction='@[-1].contactFriction')
        Surf.createObject('PointCollisionModel', name='default3', contactFriction='@[-1].contactFriction')
        Surf.createObject('SubsetMapping', name='default10', template='Vec3d,Vec3d')

        # rootNode/Floor
        Floor = rootNode.createChild('Floor')
        self.Floor = Floor
        Floor.gravity = '0 -9.81 0'
        Floor.createObject('MeshObjLoader', name='loader', filename='mesh/floor3.obj')
        Floor.createObject('MeshTopology', src='@loader', name='default11')
        Floor.createObject('MechanicalObject', scale3d='1.75 1.75 1.75', src='@loader', force='0 0 0', name='default12', free_position='0 0 0', restScale='1', free_velocity='0 0 0', template='Vec3d', velocity='0 0 0', position='0 0 0', translation='0 -10 0', derivX='0 0 0')
        Floor.createObject('TriangleCollisionModel', simulated='0', moving='0', contactFriction='0.6', template='Vec3d', name='FloorTriangle')
        Floor.createObject('LineCollisionModel', simulated='0', moving='0', contactFriction='@[-1].contactFriction', name='FloorLine')
        Floor.createObject('PointCollisionModel', simulated='0', moving='0', contactFriction='@[-1].contactFriction', name='FloorLine')
        Floor.createObject('MeshObjLoader', scale3d='1.75 1.75 1.75', handleSeams='1', translation='0 -10 0', name='meshLoader_1', filename='mesh/floor3.obj')
        Floor.createObject('OglModel', src='@meshLoader_1', texturename='textures/brushed_metal.bmp', name='FloorV', template='ExtVec3f')

        # rootNode/cubeFEM
        cubeFEM = rootNode.createChild('cubeFEM')
        self.cubeFEM = cubeFEM
        cubeFEM.gravity = '0 -9.81 0'
        cubeFEM.createObject('MechanicalObject', force='0 0 0', name='dof', free_position='0 0 0', restScale='1', free_velocity='0 0 0', template='Vec3d', position='0 0 0', velocity='0 0 0', translation='0 15 0', rotation='30 20 15', derivX='0 0 0')
        cubeFEM.createObject('UniformMass', vertexMass='0.25', name='default2', template='Vec3d')
        cubeFEM.createObject('RegularGridTopology', max='3.5 3.5 3.5', p0='-3.5 -3.5 -3.5', n='5 5 5', name='default3', min='-3.5 -3.5 -3.5')
        cubeFEM.createObject('TetrahedronFEMForceField', poissonRatio='0.3', name='FEM', computeGlobalMatrix='0', updateStiffnessMatrix='0', method='large', template='Vec3d', youngModulus='25')

        # rootNode/cubeFEM/Visu
        Visu = cubeFEM.createChild('Visu')
        self.Visu = Visu
        Visu.gravity = '0 -9.81 0'
        Visu.createObject('MeshObjLoader', scale3d='@../dof.scale3d', name='meshLoader_2', handleSeams='1', translation='@../dof.translation', rotation='@../dof.rotation', filename='mesh/smCube125.obj')
        Visu.createObject('OglModel', src='@meshLoader_2', material='Default Diffuse 1 1 0 0 1 Ambient 1 0.2 0 0 1 Specular 0 1 0 0 1 Emissive 0 1 0 0 1 Shininess 0 45', name='Visual', template='ExtVec3f')
        Visu.createObject('SubsetMapping', input='@..', name='default4', template='Vec3d,ExtVec3f', output='@Visual')

        # rootNode/cubeFEM/Surf
        Surf = cubeFEM.createChild('Surf')
        self.Surf = Surf
        Surf.gravity = '0 -9.81 0'
        Surf.createObject('MeshObjLoader', name='loader', filename='mesh/smCube125.obj')
        Surf.createObject('MeshTopology', src='@loader', name='default5')
        Surf.createObject('MechanicalObject', scale3d='@../dof.scale3d', src='@loader', force='0 0 0', name='default6', free_position='0 0 0', restScale='1', free_velocity='0 0 0', template='Vec3d', velocity='0 0 0', position='0 0 0', translation='@../dof.translation', rotation='@../dof.rotation', derivX='0 0 0')
        Surf.createObject('TriangleCollisionModel', name='default1', template='Vec3d', contactFriction='0.6')
        Surf.createObject('LineCollisionModel', name='default2', contactFriction='@[-1].contactFriction')
        Surf.createObject('PointCollisionModel', name='default3', contactFriction='@[-1].contactFriction')
        Surf.createObject('SubsetMapping', name='default10', template='Vec3d,Vec3d')

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
    myDistanceLMContactConstraint_DirectSolver = DistanceLMContactConstraint_DirectSolver(rootNode,commandLineArguments)
    return 0;