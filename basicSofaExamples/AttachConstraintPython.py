"""
AttachConstraintPython
is based on the scene 
/Users/marco.magliulo/mySofaCodes/basicSofaExamples/AttachConstraint.scn
but it uses the SofaPython plugin. 
Further informations on the usage of the plugin can be found in 
sofa/applications/plugins/SofaPython/doc/SofaPython.pdf
To launch the scene, type 
runSofa /Users/marco.magliulo/mySofaCodes/basicSofaExamples/AttachConstraintPython.py --argv 123
The sofa python plugin might have to be added in the sofa plugin manager, 
i.e. add the sofa python plugin in runSofa->Edit->PluginManager.
The arguments given after --argv can be used by accessing self.commandLineArguments, e.g. combined with ast.literal_eval to convert a string to a number.

The current file has been written by the python script
/Users/marco.magliulo/mySofaCodes/basicSofaExamples//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
Author of scn2python.py: Christoph PAULUS, christoph.paulus@inria.fr
"""

import sys
import Sofa

class AttachConstraint (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')

        # rootNode/Single
        Single = rootNode.createChild('Single')
        self.Single = Single
        Single.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        Single.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')

        # rootNode/Single/M1
        M1 = Single.createChild('M1')
        self.M1 = M1
        M1.createObject('MechanicalObject', showObject='1')
        M1.createObject('UniformMass', vertexMass='1')
        M1.createObject('RegularGridTopology', zmax='27', ymax='3', zmin='0', nx='4', ny='4', nz='28', xmax='-6', xmin='-9', ymin='0')
        M1.createObject('BoxConstraint', box='-9.1 -0.1 -0.1 -5.9 3.1 0.1')
        M1.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')

        # rootNode/AttachOneWay
        AttachOneWay = rootNode.createChild('AttachOneWay')
        self.AttachOneWay = AttachOneWay
        AttachOneWay.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        AttachOneWay.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')

        # rootNode/AttachOneWay/M1
        M1 = AttachOneWay.createChild('M1')
        self.M1 = M1
        M1.createObject('MechanicalObject')
        M1.createObject('UniformMass', vertexMass='1')
        M1.createObject('RegularGridTopology', zmax='9', ymax='3', zmin='0', nx='4', ny='4', nz='10', xmax='-1', xmin='-4', ymin='0')
        M1.createObject('BoxConstraint', box='-4.1 -0.1 -0.1 -0.9 3.1 0.1')
        M1.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')

        # rootNode/AttachOneWay/M2
        M2 = AttachOneWay.createChild('M2')
        self.M2 = M2
        M2.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        M2.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        M2.createObject('MechanicalObject')
        M2.createObject('UniformMass', vertexMass='1')
        M2.createObject('RegularGridTopology', zmax='18', ymax='3', zmin='9', nx='4', ny='4', nz='10', xmax='-1', xmin='-4', ymin='0')
        M2.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')

        # rootNode/AttachOneWay/M3
        M3 = AttachOneWay.createChild('M3')
        self.M3 = M3
        M3.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        M3.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        M3.createObject('MechanicalObject')
        M3.createObject('UniformMass', vertexMass='1')
        M3.createObject('RegularGridTopology', zmax='27', ymax='3', zmin='18', nx='4', ny='4', nz='10', xmax='-1', xmin='-4', ymin='0')
        M3.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')
        AttachOneWay.createObject('AttachConstraint', constraintFactor='1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1', object1='@M1', object2='@M2', indices1='144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159', indices2='0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15')
        AttachOneWay.createObject('AttachConstraint', constraintFactor='1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1', object1='@M2', object2='@M3', indices1='144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159', indices2='0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15')

        # rootNode/AttachTwoWay
        AttachTwoWay = rootNode.createChild('AttachTwoWay')
        self.AttachTwoWay = AttachTwoWay
        AttachTwoWay.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        AttachTwoWay.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')

        # rootNode/AttachTwoWay/M1
        M1 = AttachTwoWay.createChild('M1')
        self.M1 = M1
        M1.createObject('MechanicalObject')
        M1.createObject('UniformMass', vertexMass='1')
        M1.createObject('RegularGridTopology', zmax='9', ymax='3', zmin='0', nx='4', ny='4', nz='10', xmax='4', xmin='1', ymin='0')
        M1.createObject('BoxConstraint', box='0.9 -0.1 -0.1 4.1 3.1 0.1')
        M1.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')

        # rootNode/AttachTwoWay/M2
        M2 = AttachTwoWay.createChild('M2')
        self.M2 = M2
        M2.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        M2.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        M2.createObject('MechanicalObject')
        M2.createObject('UniformMass', vertexMass='1')
        M2.createObject('RegularGridTopology', zmax='18', ymax='3', zmin='9', nx='4', ny='4', nz='10', xmax='4', xmin='1', ymin='0')
        M2.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')

        # rootNode/AttachTwoWay/M3
        M3 = AttachTwoWay.createChild('M3')
        self.M3 = M3
        M3.createObject('EulerImplicitSolver', name='cg_odesolver', printLog='false')
        M3.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')
        M3.createObject('MechanicalObject')
        M3.createObject('UniformMass', vertexMass='1')
        M3.createObject('RegularGridTopology', zmax='27', ymax='3', zmin='18', nx='4', ny='4', nz='10', xmax='4', xmin='1', ymin='0')
        M3.createObject('TetrahedronFEMForceField', name='FEM', poissonRatio='0.3', youngModulus='4000')
        AttachTwoWay.createObject('AttachConstraint', object1='@M1', object2='@M2', indices1='144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159', indices2='0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15', constraintFactor='1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1', twoWay='true')
        AttachTwoWay.createObject('AttachConstraint', object1='@M2', object2='@M3', indices1='144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159', twoWay='true', indices2='0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15')

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
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myAttachConstraint = AttachConstraint(rootNode,commandLineArguments)
    return 0;