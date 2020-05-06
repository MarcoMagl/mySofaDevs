"""
DOFBlockerLMConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/DOFBlockerLMConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/DOFBlockerLMConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class DOFBlockerLMConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showForceFields showBoundingCollisionModels')
        rootNode.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='default26', rayleighMass='0.1')
        rootNode.createObject('LMConstraintSolver', constraintPos='1', numIterations='27', maxError='1e-7', constraintVel='1', name='ConstraintSolver')
        rootNode.createObject('CGLinearSolver', threshold='1e-07', tolerance='1e-07', template='GraphScattered', iterations='25', name='default31')

        # rootNode/CubeFree
        CubeFree = rootNode.createChild('CubeFree')
        self.CubeFree = CubeFree
        CubeFree.gravity = '0 -9.81 0'
        CubeFree.createObject('MechanicalObject', velocity='0 0 0 0 2 0', translation='0 0 0', name='wY=2', template='Rigid3d', restScale='1')
        CubeFree.createObject('UncoupledConstraintCorrection', name='default67', template='Rigid3d')
        CubeFree.createObject('UniformMass', vertexMass='10 1 [1 0 0,0 1 0,0 0 1]', name='default17', template='Rigid3d', totalMass='2')

        # rootNode/CubeFree/Visu
        Visu = CubeFree.createChild('Visu')
        self.Visu = Visu
        Visu.gravity = '0 -9.81 0'
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_1', filename='mesh/cube.obj')
        Visu.createObject('OglModel', src='@meshLoader_1', material='Default Diffuse 1 1 0.5 0.25 1 Ambient 1 0.2 0.1 0.05 1 Specular 0 1 0.5 0.25 1 Emissive 0 1 0.5 0.25 1 Shininess 0 45', name='Visual', template='ExtVec3f')
        Visu.createObject('RigidMapping', input='@..', name='default19', template='Rigid,ExtVec3f', output='@Visual')

        # rootNode/CubeFree/Surf2
        Surf2 = CubeFree.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.gravity = '0 -9.81 0'
        Surf2.createObject('MeshObjLoader', name='meshLoader1', filename='mesh/cube.obj')
        Surf2.createObject('MeshTopology', src='@meshLoader1', tags='LDI', name='default20', triangles='4 0 7  0 3 7  2 6 7  2 7 3  1 5 2  5 6 2  0 4 1  4 5 1  4 7 6  4 6 5  0 1 2  0 2 3 ', position='1 -1 -1 1 -1 1 -1 -1 1 -1 -1 -1 1 1 -1 0.999999 1 1 -1 1 1 -1 1 -1')
        Surf2.createObject('MechanicalObject', name='default21', template='Vec3d', restScale='1')
        Surf2.createObject('RigidMapping', name='default22', template='Rigid,Vec3d')
        Surf2.createObject('TriangleCollisionModel', name='FrictionCoeff', contactFriction='1')

        # rootNode/RotationConstrained
        RotationConstrained = rootNode.createChild('RotationConstrained')
        self.RotationConstrained = RotationConstrained
        RotationConstrained.gravity = '0 -9.81 0'
        RotationConstrained.createObject('MechanicalObject', velocity='0 0 0 0 2 0', translation='3 0 0', name='wY=2', template='Rigid3d', restScale='1')
        RotationConstrained.createObject('UncoupledConstraintCorrection', name='default67', template='Rigid3d')
        RotationConstrained.createObject('UniformMass', vertexMass='10 1 [1 0 0,0 1 0,0 0 1]', name='default17', template='Rigid3d', totalMass='2')

        # rootNode/RotationConstrained/Visu
        Visu = RotationConstrained.createChild('Visu')
        self.Visu = Visu
        Visu.gravity = '0 -9.81 0'
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_0', filename='mesh/cube.obj')
        Visu.createObject('OglModel', src='@meshLoader_0', material='Default Diffuse 1 1 0.5 0.25 1 Ambient 1 0.2 0.1 0.05 1 Specular 0 1 0.5 0.25 1 Emissive 0 1 0.5 0.25 1 Shininess 0 45', name='Visual', template='ExtVec3f')
        Visu.createObject('RigidMapping', input='@..', name='default19', template='Rigid,ExtVec3f', output='@Visual')

        # rootNode/RotationConstrained/Surf2
        Surf2 = RotationConstrained.createChild('Surf2')
        self.Surf2 = Surf2
        Surf2.gravity = '0 -9.81 0'
        Surf2.createObject('MeshObjLoader', name='meshLoader0', filename='mesh/cube.obj')
        Surf2.createObject('MeshTopology', src='@meshLoader0', tags='LDI', name='default20', triangles='4 0 7  0 3 7  2 6 7  2 7 3  1 5 2  5 6 2  0 4 1  4 5 1  4 7 6  4 6 5  0 1 2  0 2 3 ', position='1 -1 -1 1 -1 1 -1 -1 1 -1 -1 -1 1 1 -1 0.999999 1 1 -1 1 1 -1 1 -1')
        Surf2.createObject('MechanicalObject', name='default21', template='Vec3d', restScale='1')
        Surf2.createObject('RigidMapping', name='default22', template='Rigid,Vec3d')
        Surf2.createObject('TriangleCollisionModel', name='FrictionCoeff', contactFriction='1')
        RotationConstrained.createObject('DOFBlockerLMConstraint', factorAxis='1', indices='0', name='RotationConstraint', template='Rigid3d', rotationAxis='0 0 0 0 1 0 0 0 0 0 0 1')

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
    rootNode.findData('gravity').value = '0 0 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myDOFBlockerLMConstraint = DOFBlockerLMConstraint(rootNode,commandLineArguments)
    return 0;