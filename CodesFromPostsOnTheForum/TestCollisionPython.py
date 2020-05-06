"""
TestCollisionPython
--> I used this forum post: https://www.sofa-framework.org/community/forum/topic/crash-in-collision-response-computation/
"""

import sys
import Sofa

class TestCollision (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        # rootNode
        rootNode.createObject('RequiredPlugin', pluginName='SofaSparseSolver', name='SofaSparseSolver')
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        rootNode.createObject('FreeMotionAnimationLoop')
        rootNode.createObject('GenericConstraintSolver', maxIterations='1000', tolerance='0.001')
        rootNode.createObject('DefaultPipeline', draw='0', verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject('MinProximityIntersection', contactDistance='1e-1', alarmDistance='2e-1', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='CollisionResponse', response='FrictionContact')


        # rootNode/Beams
        Beams = rootNode.createChild('Beams')
        self.Beams = Beams
        Beams.createObject('EulerImplicitSolver', printLog='false', rayleighStiffness='0.1', name='odesolver', rayleighMass='0.1')
        Beams.createObject('SparseLUSolver', verbose='true')
        position = '0 0 0 0 0 0 1 1 0 0 0 0 0 1 2 0 0 0 0 0 1 3 0 0 0 0 0 1 4 0 0 0 0 0 1 5 0 0 0 0 0 1 6 0 0 0 0 0 1 7 0 0 0 0 0 1 0 0 0 0 0 -0.707107 0.707107 0 -1 0 0 0-0.707107 0.707107 0 -2 0 0 0 -0.707107 0. 0 -3 0 0 0 -0.707107 0.707107 0 -4 0 0 0 -0.707107 0. 0 -5 0 0 0 -0.707107 0.707107                                                                     0 -6 0 0 0 -0.707107 0.707107 0 -7 0 0 0 -0.707107 0.707107'
        Beams.createObject('MechanicalObject', position=position, name='DOFs', template='Rigid3d')
        Beams.createObject('MeshTopology', lines='0 1 1 2 2 3 3 4 4 5 5 6 6 7  8 9 9 10 10 11 11 12 12 13 13 14 14 15', name='lines')
        Beams.createObject('UniformMass', showAxisSizeFactor='1e-1', printLog='false', totalMass='1')
        Beams.createObject('BeamFEMForceField', radius='0.1', name='FEM', poissonRatio='0.3', youngModulus='2e11')
        Beams.createObject('FixedConstraint', indices='7', name='FixedConstraint')
        Beams.createObject('LinearSolverConstraintCorrection')
        Beams.createObject('BilateralInteractionConstraint', object1='@DOFs', first_point='0', template='Rigid3d', keepOrientationDifference='1', second_point='8', object2='@DOFs')
        Beams.createObject('ConstantForceField', indices='15', showColor='0.961 0.635 0.906', name='FF', showArrowSize='0.00001', forces='100000 0 0 0 0 0')

        # rootNode/Beams/Collision
        Collision = Beams.createChild('Collision')
        self.Collision = Collision
        Collision.createObject('MechanicalObject', position='0 0 0                                                                                 1 0 0                                                                                 2 0 0                                                                                 3 0 0                                                                                 4 0 0                                                                                 5 0 0                                                                                 6 0 0                                                                                 7 0 0                                                                                 0 0 0                                                                                 0 -1 0                                                                                 0 -2 0                                                                                 0 -3 0                                                                                 0 -4 0                                                                                 0 -5 0                                                                                 0 -6 0                                                                                 0 -7 0', name='collisionDOFs', template='Vec3d')
        Collision.createObject('MeshTopology', lines='0 1 1 2 2 3 3 4 4 5 5 6 6 7  8 9 9 10 10 11 11 12 12 13 13 14 14 15', name='lines')
        Collision.createObject('TLineModel', name='beamLine', template='Vec3d')
        Collision.createObject('TPointModel', name='beamPoint')
        Collision.createObject('IdentityMapping')

        # rootNode/Floor
        Floor = rootNode.createChild('Floor')
        self.Floor = Floor
        Floor.createObject('MeshObjLoader', translation='0 -9.25 0', scale='0.1', name='loader', filename='floor2b.obj')
        Floor.createObject('MeshTopology', src='@loader', name='floorTopo')
        Floor.createObject('MechanicalObject', src='@loader', name='floorDoFs')
        Floor.createObject('TTriangleModel', moving='0', name='floorTriangle', simulated='0')

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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/CodesFromPostsOnTheForum//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = '0.0002'
    rootNode.findData('gravity').value = '0 -9.81 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myTestCollision = TestCollision(rootNode,commandLineArguments)
    return 0;