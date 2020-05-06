"""
Compare_FixConstraintsPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/Compare_FixConstraints.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/Compare_FixConstraintsPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class Compare_FixConstraints (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('VisualStyle', displayFlags='showBehavior')

        # rootNode/FixedConstraint
        FixedConstraint = rootNode.createChild('FixedConstraint')
        self.FixedConstraint = FixedConstraint
        FixedConstraint.createObject('EulerImplicitSolver', rayleighStiffness='0.1', rayleighMass='0.1')
        FixedConstraint.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', iterations='25')

        # rootNode/FixedConstraint/unnamedNode_0
        unnamedNode_0 = FixedConstraint.createChild('unnamedNode_0')
        self.unnamedNode_0 = unnamedNode_0
        unnamedNode_0.createObject('RegularGridTopology')
        unnamedNode_0.createObject('MechanicalObject', showIndices='1', showIndicesScale='0.04')
        unnamedNode_0.createObject('HexahedronFEMForceField', poissonRatio='0', youngModulus='1000')
        unnamedNode_0.createObject('BoxROI', box='0 0.75 0 1 1 1', position='@[-2].rest_position')
        unnamedNode_0.createObject('FixedConstraint', indices='@[-1].indices')
        unnamedNode_0.createObject('ConstantForceField', indices='0 1 4 5', totalForce='0 -1000 0')
        unnamedNode_0.createObject('UniformMass')

        # rootNode/FixedLMConstraint
        FixedLMConstraint = rootNode.createChild('FixedLMConstraint')
        self.FixedLMConstraint = FixedLMConstraint
        FixedLMConstraint.createObject('EulerImplicitSolver')
        FixedLMConstraint.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', iterations='25')
        FixedLMConstraint.createObject('LMConstraintSolver', maxError='1e-7', numIterations='27')
        FixedLMConstraint.createObject('VisualStyle', displayFlags='showBehavior')

        # rootNode/FixedLMConstraint/unnamedNode_0
        unnamedNode_0 = FixedLMConstraint.createChild('unnamedNode_0')
        self.unnamedNode_0 = unnamedNode_0
        unnamedNode_0.createObject('RegularGridTopology', p0='2 0 0')
        unnamedNode_0.createObject('MechanicalObject', showIndices='1', showIndicesScale='0.0004')
        unnamedNode_0.createObject('HexahedronFEMForceField', poissonRatio='0', youngModulus='1000')
        unnamedNode_0.createObject('BoxROI', box='2 0.75 0 3 1 1', position='@[-2].rest_position')
        unnamedNode_0.createObject('FixedLMConstraint', indices='@[-1].indices', drawsize='0.1')
        unnamedNode_0.createObject('ConstantForceField', indices='0 1 4 5', totalForce='0 -1000 0')
        unnamedNode_0.createObject('UniformMass')

        # rootNode/DOFBlockerAllAxis
        DOFBlockerAllAxis = rootNode.createChild('DOFBlockerAllAxis')
        self.DOFBlockerAllAxis = DOFBlockerAllAxis
        DOFBlockerAllAxis.createObject('EulerImplicitSolver')
        DOFBlockerAllAxis.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', iterations='25')
        DOFBlockerAllAxis.createObject('LMConstraintSolver', maxError='1e-7', numIterations='27')
        DOFBlockerAllAxis.createObject('VisualStyle', displayFlags='showBehavior')

        # rootNode/DOFBlockerAllAxis/unnamedNode_0
        unnamedNode_0 = DOFBlockerAllAxis.createChild('unnamedNode_0')
        self.unnamedNode_0 = unnamedNode_0
        unnamedNode_0.createObject('RegularGridTopology', p0='4 0 0')
        unnamedNode_0.createObject('MechanicalObject', showIndices='1', showIndicesScale='0.0004')
        unnamedNode_0.createObject('HexahedronFEMForceField', poissonRatio='0', youngModulus='1000')
        unnamedNode_0.createObject('BoxROI', box='4 0.75 0 5 1 1', position='@[-2].rest_position', indices='0')
        unnamedNode_0.createObject('ConstantForceField', indices='0 1 4 5', totalForce='0 -1000 0')
        unnamedNode_0.createObject('UniformMass')
        unnamedNode_0.createObject('DOFBlockerLMConstraint', indices='@[-3].indices', rotationAxis='1 0 0 0 1 0 0 0 1')

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
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myCompare_FixConstraints = Compare_FixConstraints(rootNode,commandLineArguments)
    return 0;