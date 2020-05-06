"""
ConstantForceFieldPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/basicSofaExamples/ConstantForceField.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/basicSofaExamples/ConstantForceFieldPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class ConstantForceField (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')

        # rootNode/BasicDeformableObject
        BasicDeformableObject = rootNode.createChild('BasicDeformableObject')
        self.BasicDeformableObject = BasicDeformableObject
        BasicDeformableObject.createObject('EulerImplicitSolver', printLog='false', name='cg_odesolver', rayleighMass='0.1')
        BasicDeformableObject.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        BasicDeformableObject.createObject('MechanicalObject', position='0 0 0  1 0 0  1 1 0  0 1 0', velocity='0 0 0  0 0 0  0 0 0  0 0 0')
        BasicDeformableObject.createObject('UniformMass', vertexMass='0.1')
        BasicDeformableObject.createObject('MeshTopology', triangles='0 1 2  0 2 3')
        BasicDeformableObject.createObject('TriangleFEMForceField', youngModulus='100', method='large', poissonRatio='0.3', name='FEM0')
        BasicDeformableObject.createObject('ConstantForceField', indices='0 1 2 3', showArrowSize='0.5', printLog='1', forces='-1 -1 0  1 -1 0  1 1 0  -1 1 0')

        # rootNode/BasicDeformableObject/Visu
        Visu = BasicDeformableObject.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('OglModel', color='red', name='Visual')
        Visu.createObject('IdentityMapping', input='@..', output='@Visual')

        # rootNode/TorusRigid
        TorusRigid = rootNode.createChild('TorusRigid')
        self.TorusRigid = TorusRigid
        TorusRigid.createObject('EulerImplicitSolver', rayleighStiffness='0.01')
        TorusRigid.createObject('CGLinearSolver', threshold='0.00000001', tolerance='1e-5', iterations='25')
        TorusRigid.createObject('MechanicalObject', scale='1.0', dx='2', rx='0', ry='0', rz='0', dz='0', template='Rigid3d', dy='0')
        TorusRigid.createObject('UniformMass')
        TorusRigid.createObject('ConstantForceField', indices='0', forces='0 0.10 0     0 1 0 0')

        # rootNode/TorusRigid/Visu
        Visu = TorusRigid.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('MeshObjLoader', handleSeams='1', scale='0.3', name='meshLoader_0', filename='mesh/torus.obj')
        Visu.createObject('OglModel', color='gray', src='@meshLoader_0', name='Visual')
        Visu.createObject('RigidMapping', input='@..', output='@Visual')

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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = '0.05'
    rootNode.findData('gravity').value = '0 0 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myConstantForceField = ConstantForceField(rootNode,commandLineArguments)
    return 0;