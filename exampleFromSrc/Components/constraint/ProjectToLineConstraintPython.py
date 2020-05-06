"""
ProjectToLineConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/ProjectToLineConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint/ProjectToLineConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/exampleFromSrc/Components/constraint//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class ProjectToLineConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('VisualStyle', displayFlags='hideVisualModels showBehavior')

        # rootNode/Square
        Square = rootNode.createChild('Square')
        self.Square = Square
        Square.createObject('EulerImplicitSolver', rayleighStiffness='0.5', vdamping='0', verbose='0', name='Euler Implicit', printLog='0', rayleighMass='0.5')
        Square.createObject('CGLinearSolver', verbose='0', iterations='40', threshold='1e-10', printLog='0', tolerance='1e-06', template='GraphScattered', name='CG Solver')
        Square.createObject('GridMeshCreator', rotation='0 0 0 ', scale='1 1 0', resolution='5 5', name='loader', trianglePattern='1')
        Square.createObject('MechanicalObject', position='@loader.position', showIndicesScale='0.001', name='mObject1', template='Vec3d', showIndices='false')
        Square.createObject('TriangleSetTopologyContainer', position='@loader.position', edges='@loader.edges', name='Container', triangles='@loader.triangles')
        Square.createObject('TriangleSetTopologyModifier', name='Modifier')
        Square.createObject('TriangleSetTopologyAlgorithms', name='TopoAlgo', template='Vec3d')
        Square.createObject('TriangleSetGeometryAlgorithms', name='GeomAlgo', template='Vec3d')
        Square.createObject('UniformMass', template='Vec3d')
        Square.createObject('TriangularFEMForceField', method='large', template='Vec3d', name='FEM', poissonRatio='0.3', youngModulus='20')
        Square.createObject('BoxConstraint', box='-0.05 -0.05 -0.05    0.05 0.05 0.05', drawBoxes='1')
        Square.createObject('BoxROI', box='-0.05 -0.05 -0.05    0.05 1.05 0.05', drawBoxes='1', name='ProjectToLine')
        Square.createObject('ProjectToLineConstraint', indices='@[-1].indices', drawSize='0.03', direction='0.1 1 0')

        # rootNode/Square/Boundary Edges
        Boundary_Edges = Square.createChild('Boundary Edges')
        self.Boundary_Edges = Boundary_Edges
        Boundary_Edges.createObject('EdgeSetTopologyContainer', name='Container')
        Boundary_Edges.createObject('EdgeSetTopologyModifier', name='Modifier')
        Boundary_Edges.createObject('EdgeSetTopologyAlgorithms', name='TopoAlgo', template='Vec3d')
        Boundary_Edges.createObject('EdgeSetGeometryAlgorithms', drawEdges='1', name='GeomAlgo', template='Vec3d')
        Boundary_Edges.createObject('Triangle2EdgeTopologicalMapping', input='@../Container', name='Mapping', output='@Container')
        Boundary_Edges.createObject('BoxROI', box='0.95 -0.05 -0.05    1.05 1.05 0.05', drawEdges='1', edges='@Container.edges', drawBoxes='1', name='pressureBox', position='@../mObject1.rest_position')
        Boundary_Edges.createObject('EdgePressureForceField', showForces='1', name='edgePressureFF0', arrowSizeCoef='1', binormal='0 0 1', p_intensity='-10', template='Vec3d', edgeIndices='@pressureBox.edgeIndices')

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
    rootNode.findData('dt').value = '0.05'
    rootNode.findData('gravity').value = '0 0 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myProjectToLineConstraint = ProjectToLineConstraint(rootNode,commandLineArguments)
    return 0;