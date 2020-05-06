"""
InextensiblePendulumPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/InextensiblePendulum.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/InextensiblePendulumPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class InextensiblePendulum (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaSparseSolver')
        rootNode.createObject('VisualStyle', displayFlags='hideVisualModels showBehaviorModels showMappings showForceFields')
        rootNode.createObject('FreeMotionAnimationLoop', solveVelocityConstraintFirst='true')
        rootNode.createObject('GenericConstraintSolver', maxIterations='1000', tolerance='1e-9')
        rootNode.createObject('StringMeshCreator', scale3d='1 1 1', resolution='20', name='loader')

        # rootNode/withImplicitConstraintForce
        withImplicitConstraintForce = rootNode.createChild('withImplicitConstraintForce')
        self.withImplicitConstraintForce = withImplicitConstraintForce
        withImplicitConstraintForce.createObject('TransformEngine', translation='0 0 0', input_position='@../loader.position', name='translate')
        withImplicitConstraintForce.createObject('EulerImplicitSolver')
        withImplicitConstraintForce.createObject('SparseCholeskySolver')
        withImplicitConstraintForce.createObject('GenericConstraintCorrection')
        withImplicitConstraintForce.createObject('EdgeSetTopologyContainer', position='@translate.output_position', edges='@../loader.edges')
        withImplicitConstraintForce.createObject('MechanicalObject', name='defoDOF', template='Vec3d')
        withImplicitConstraintForce.createObject('EdgeSetGeometryAlgorithms', drawEdges='true')
        withImplicitConstraintForce.createObject('FixedConstraint', indices='0')
        withImplicitConstraintForce.createObject('DiagonalMass', name='mass', totalMass='1e-3')
        withImplicitConstraintForce.createObject('MappingGeometricStiffnessForceField', mapping='@./extensionsNode/distanceMapping')

        # rootNode/withImplicitConstraintForce/extensionsNode
        extensionsNode = withImplicitConstraintForce.createChild('extensionsNode')
        self.extensionsNode = extensionsNode
        extensionsNode.createObject('MechanicalObject', name='extensionsDOF', template='Vec1d')
        extensionsNode.createObject('DistanceMapping', name='distanceMapping')
        extensionsNode.createObject('UniformConstraint', iterative='false', template='Vec1d')

        # rootNode/withoutImplicitConstraintForce
        withoutImplicitConstraintForce = rootNode.createChild('withoutImplicitConstraintForce')
        self.withoutImplicitConstraintForce = withoutImplicitConstraintForce
        withoutImplicitConstraintForce.createObject('TransformEngine', translation='0 0 -2', input_position='@../loader.position', name='translate')
        withoutImplicitConstraintForce.createObject('EulerImplicitSolver')
        withoutImplicitConstraintForce.createObject('SparseCholeskySolver')
        withoutImplicitConstraintForce.createObject('GenericConstraintCorrection')
        withoutImplicitConstraintForce.createObject('EdgeSetTopologyContainer', position='@translate.output_position', edges='@../loader.edges')
        withoutImplicitConstraintForce.createObject('MechanicalObject', name='defoDOF', template='Vec3d')
        withoutImplicitConstraintForce.createObject('EdgeSetGeometryAlgorithms', drawEdges='true')
        withoutImplicitConstraintForce.createObject('FixedConstraint', indices='0')
        withoutImplicitConstraintForce.createObject('DiagonalMass', name='mass', totalMass='1e-3')

        # rootNode/withoutImplicitConstraintForce/extensionsNode
        extensionsNode = withoutImplicitConstraintForce.createChild('extensionsNode')
        self.extensionsNode = extensionsNode
        extensionsNode.createObject('MechanicalObject', name='extensionsDOF', template='Vec1d')
        extensionsNode.createObject('DistanceMapping', name='distanceMapping')
        extensionsNode.createObject('UniformConstraint', iterative='false', template='Vec1d')

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
    rootNode.findData('gravity').value = '0 -10 0'
    rootNode.findData('animate').value = '0'
    rootNode.findData('dt').value = '0.01'
    rootNode.findData('time').value = '0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myInextensiblePendulum = InextensiblePendulum(rootNode,commandLineArguments)
    return 0;