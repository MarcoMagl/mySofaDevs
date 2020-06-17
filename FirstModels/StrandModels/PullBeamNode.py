import sys
import Sofa
import numpy as np

class BeamFEMForceField (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):
        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='Compliant')
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('MinProximityIntersection', contactDistance='0.02', alarmDistance='0.03', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='default')
        # radius of the beam
        radius = 0.1
        # heigth of the strand 
        nn = 10
        nbeam = nn - 1
        # topology
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        lines = str(lines.flatten()).replace('[', '').replace(']','')

        number_dofs_per_node = 7
        Coord = np.zeros((nn, number_dofs_per_node),dtype=float)
        Coord[:,:3] = np.array([[ 0.        ,  0.        ,  0.        ],
                      [ 0.        ,  0.        ,  0.34906585],
                      [ 0.        ,  0.        ,  0.6981317 ],
                      [ 0.        ,  0.        ,  1.04719755],
                      [ 0.        ,  0.        ,  1.3962634 ],
                      [ 0.        ,  0.        ,  1.74532925],
                      [ 0.        ,  0.        ,  2.0943951 ],
                      [ 0.        ,  0.        ,  2.44346095],
                      [ 0.        ,  0.        ,  2.7925268 ],
                      [ 0.        ,  0.        ,  3.14159265]])
        Coord[:,3:] = np.array([[ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678],
                      [ 0.        , -0.70710678,  0.        ,  0.70710678]])
        strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')

        # rootNode/beamI --> straight beam
        beamI = rootNode.createChild('beamI')
        self.beamI = beamI
        beamI.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        beamI.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
        beamI.createObject('MechanicalObject', position=strCoord, name='DOFs', template='Rigid3d')
        beamI.createObject('MeshTopology', lines=lines, name='lines')
        beamI.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        beamI.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false')
        beamI.createObject('BeamFEMForceField', radius=str(radius), name='FEM', poissonRatio='0.49', youngModulus='20000000')
        keyTimes = '0 2' 
        movements = '0 0 0 0 0 0   0 0 0.1 0 0 0'
        beamI.createObject('LinearMovementConstraint', keyTimes=keyTimes, template='Rigid3d', movements=movements, indices=str(nn-1))

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
    rootNode.findData('dt').value = '0.01'
    rootNode.findData('gravity').value = '0 0 -9.81'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myBeamFEMForceField = BeamFEMForceField(rootNode,commandLineArguments)
    return 0;