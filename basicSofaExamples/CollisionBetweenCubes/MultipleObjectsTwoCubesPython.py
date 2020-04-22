"""
MultipleObjectsTwoCubesPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes/MultipleObjectsTwoCubes.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes/MultipleObjectsTwoCubesPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class MultipleObjectsTwoCubes (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('VisualStyle', displayFlags='showBehavior showCollisionModels')
        rootNode.createObject('DefaultPipeline')
        rootNode.createObject('BruteForceDetection')
        rootNode.createObject('DefaultContactManager')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.5', alarmDistance='1')

        # rootNode/Cube1
        Cube1 = rootNode.createChild('Cube1')
        self.Cube1 = Cube1
        Cube1.createObject('EulerImplicitSolver', rayleighStiffness='0.1', name='EulerImplicit Cube1', rayleighMass='0.1')
        Cube1.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', name='CG Solver Cube1', iterations='25')
        Cube1.createObject('MechanicalObject', position='0 0 1  1 0 1  0 1 1  1 1 1  0 0 2  1 0 2  0 1 2  1 1 2', translation='0.5 2 0', name='Particles Cube1', template='Vec3d')
        Cube1.createObject('MeshTopology', hexas='0 4 6 2 1 5 7 3', name='Topology Cube1')
        Cube1.createObject('UniformMass', name='Mass Cube1', totalMass='1')
        Cube1.createObject('MeshSpringForceField', name='Springs Cube1', stiffness='100', damping='1')
        Cube1.createObject('SphereModel', radius='0.2', name='Spheres For Collision Cube1')

        # rootNode/Cube2
        Cube2 = rootNode.createChild('Cube2')
        self.Cube2 = Cube2
        Cube2.createObject('EulerImplicitSolver', name='EulerImplicit Cube2')
        Cube2.createObject('CGLinearSolver', threshold='1e-5', tolerance='1e-5', name='CG Solver Cube2', iterations='25')
        Cube2.createObject('MechanicalObject', position='0 0 1  1 0 1  0 1 1  1 1 1  0 0 2  1 0 2  0 1 2  1 1 2', name='Particles Cube2', template='Vec3d')
        Cube2.createObject('MeshTopology', hexas='0 4 6 2 1 5 7 3', name='Topology Cube2')
        Cube2.createObject('UniformMass', name='Mass Cube2', totalMass='1')
        Cube2.createObject('MeshSpringForceField', name='Springs Cube2', stiffness='15', damping='1')
        Cube2.createObject('TriangleCollisionModel', name='Triangles For Collision')
        Cube2.createObject('LineCollisionModel', name='Lines For Collision')
        Cube2.createObject('PointCollisionModel', name='Points For Collision')

        # rootNode/Floor
        Floor = rootNode.createChild('Floor')
        self.Floor = Floor
        Floor.createObject('MeshTopology', name='Topology Floor', filename='mesh/floor.obj')
        Floor.createObject('MechanicalObject', name='Particles Floor')
        Floor.createObject('TriangleCollisionModel', moving='0', name='Triangle For Collision Floor', simulated='0')

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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/basicSofaExamples/CollisionBetweenCubes//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = '0.01'
    rootNode.findData('gravity').value = '0 -9.81 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myMultipleObjectsTwoCubes = MultipleObjectsTwoCubes(rootNode,commandLineArguments)
    return 0;