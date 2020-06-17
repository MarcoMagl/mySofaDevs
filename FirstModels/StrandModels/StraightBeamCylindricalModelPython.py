"""
StraightBeamCylindricalModelPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/StrandModels/StraightBeamCylindricalModel.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/StrandModels/StraightBeamCylindricalModelPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa
import numpy as np

class StraightBeamCylindricalModel (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        # rootNode
        rootNode.createObject('EulerImplicit', rayleighStiffness='0.1', printLog='false')
        rootNode.createObject('CGLinearSolver', threshold='1e-2', tolerance='1e-5', template='GraphScattered', iterations='20')

        nn = 10
        nbeam= nn - 1
        L = 5
        Coord = np.zeros((nn, 7),dtype=float)
        Coord[:,0] = np.linspace(0,L,nn)
        Coord[:,2] = 0
        Coord[:,1] = 0 
        Coord[:,3:] = [0,0,0,1]
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        lines = str(lines.flatten()).replace('[', '').replace(']','')
        beam = rootNode.createChild('beam')
        self.beam = beam
        # beam.createObject('MechanicalObject', position=strCoord, rotation='0 -90 0', name='catheterDOFs', template='Vec3')
        beam.createObject('MechanicalObject', position=strCoord,  name='catheterDOFs', template='Rigid3d')
        beam.createObject('MeshTopology', lines=lines, name='lines')
        beam.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beam.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beam.createObject('BeamFEMForceField', radius=str(0.1), name='FEM', poissonRatio='0.49', youngModulus='10000000')
        # # rlision.createObject('Point')
        # rootNode/visu
        visu = beam.createChild('visu')
        self.visu = visu
        # visu.createObject('CylinderGridTopology', nx='4', ny='4', length=str(2*L), radius='0.3', name='coli', nz='10', axis='1 0 0')
        visu.createObject('CylinderGridTopology', nx='4', ny='4', length=str(2*L), radius='0.3', name='coli', nz='10')
        visu.createObject('OglModel', color='gray')
        visu.createObject('BeamLinearMapping', isMechanical='true')

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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/StrandModels//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('gravity').value = '0 9.8 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myStraightBeamCylindricalModel = StraightBeamCylindricalModel(rootNode,commandLineArguments)
    return 0;