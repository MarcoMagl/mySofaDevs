"""
EllipsoidForceFieldPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted/EllipsoidForceField.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted/EllipsoidForceFieldPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class EllipsoidForceField (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('VisualStyle', displayFlags='showForceFields showVisual')
        rootNode.createObject('DefaultPipeline', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('DefaultContactManager', name='Response')
        rootNode.createObject('NewProximityIntersection', contactDistance='0.001', alarmDistance='0.002')

        # rootNode/SquareCloth1
        SquareCloth1 = rootNode.createChild('SquareCloth1')
        self.SquareCloth1 = SquareCloth1
        SquareCloth1.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        SquareCloth1.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        SquareCloth1.createObject('MechanicalObject')
        SquareCloth1.createObject('UniformMass', totalMass='100')
        SquareCloth1.createObject('RegularGrid', zmax='12', ymax='7', zmin='-12', nx='20', ny='1', nz='20', xmax='-12', xmin='12', ymin='7')
        SquareCloth1.createObject('BoxROI', box='-12 7 12 -10 7 12', name="BoxForConstraint1")
        SquareCloth1.createObject('BoxROI', box='10 7 12 12 7 12', name="BoxForConstraint2")
        SquareCloth1.createObject('FixedConstraint', indices="@BoxForConstraint1.indices", name='FixedCstr1')
        SquareCloth1.createObject('FixedConstraint', indices="@BoxForConstraint2.indices", name='FixedCstr2')
        SquareCloth1.createObject('MeshSpringForceField', name='Springs', stiffness='2000', damping='0')
        SquareCloth1.createObject('QuadBendingSprings', name='Bend', stiffness='20', damping='0')
        SquareCloth1.createObject('EllipsoidForceField', center='0 5 3', damping='1', stiffness='1000', vradius='6 2 6')

        # rootNode/SquareCloth1/Visu
        Visu = SquareCloth1.createChild('Visu')
        self.Visu = Visu
        Visu.createObject('OglModel', color='green', name='Visual')
        Visu.createObject('IdentityMapping', input='@..', output='@Visual')

        # rootNode/SquareCloth1/unnamedNode_0
        unnamedNode_0 = SquareCloth1.createChild('unnamedNode_0')
        self.unnamedNode_0 = unnamedNode_0
        unnamedNode_0.createObject('RegularGrid', zmax='12', ymax='7', zmin='-12', nx='4', ny='1', nz='4', xmax='-12', xmin='12', ymin='7')
        unnamedNode_0.createObject('MechanicalObject')
        unnamedNode_0.createObject('SphereModel', contactStiffness='1', radius='1.0')
        unnamedNode_0.createObject('SubsetMapping', radius='0.8')

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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = '0.04'
    rootNode.findData('gravity').value = '0.0 -2.0 0.0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myEllipsoidForceField = EllipsoidForceField(rootNode,commandLineArguments)
    return 0;