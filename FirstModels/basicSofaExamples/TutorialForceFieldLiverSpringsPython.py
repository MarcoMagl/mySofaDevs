"""
TutorialForceFieldLiverSpringsPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/basicSofaExamples/TutorialForceFieldLiverSprings.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/basicSofaExamples/TutorialForceFieldLiverSpringsPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class TutorialForceFieldLiverSprings (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('VisualStyle', displayFlags='showForceFields')
        rootNode.createObject('DefaultPipeline', name='CollisionPipeline', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('DefaultContactManager', name='collision response', response='default')
        rootNode.createObject('DiscreteIntersection')

        # rootNode/Liver
        Liver = rootNode.createChild('Liver')
        self.Liver = Liver
        Liver.gravity = '0 -9.81 0'
        Liver.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        Liver.createObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='25', template='GraphScattered')
        Liver.createObject('MeshGmshLoader', name='meshLoader0', filename='mesh/liver.msh')
        Liver.createObject('MeshTopology', src='@meshLoader0', name='mesh')
        Liver.createObject('MechanicalObject', name='dofs', template='Vec3d')
        Liver.createObject('MeshSpringForceField', name='Springs', stiffness='4500', template='Vec3d')
        Liver.createObject('UniformMass', name='mass', template='Vec3d')
        Liver.createObject('FixedConstraint', indices='3 39 64', name='FixedConstraint', template='Vec3d')

        # rootNode/Liver/Visu
        Visu = Liver.createChild('Visu')
        self.Visu = Visu
        Visu.gravity = '0 -9.81 0'
        Visu.createObject('MeshObjLoader', handleSeams='1', name='meshLoader_0', filename='mesh/liver-smooth.obj')
        Visu.createObject('OglModel', src='@meshLoader_0', material='Default Diffuse 1 1 0 0 1 Ambient 1 0.2 0 0 1 Specular 0 1 0 0 1 Emissive 0 1 0 0 1 Shininess 0 45', name='VisualModel', template='ExtVec3f')
        Visu.createObject('BarycentricMapping', input='@..', name='visual mapping', template='Vec3d,ExtVec3f', output='@VisualModel')

        # rootNode/Liver/Surf
        Surf = Liver.createChild('Surf')
        self.Surf = Surf
        Surf.gravity = '0 -9.81 0'
        Surf.createObject('SphereLoader', filename='mesh/liver.sph')
        Surf.createObject('MechanicalObject', position='@[-1].position')
        Surf.createObject('SphereCollisionModel', listRadius='@[-2].listRadius')
        Surf.createObject('BarycentricMapping', name='sphere mapping')

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
    rootNode.findData('dt').value = '0.02'
    rootNode.findData('gravity').value = '0 -9.81 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myTutorialForceFieldLiverSprings = TutorialForceFieldLiverSprings(rootNode,commandLineArguments)
    return 0;