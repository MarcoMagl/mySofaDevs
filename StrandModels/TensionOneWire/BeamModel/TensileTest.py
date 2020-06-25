import sys
import os
import Sofa
import numpy as np
from pyquaternion import Quaternion
import pickle 

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def getOrientationQuaternion(a, b):
    assert np.allclose(np.linalg.norm(b), 1.)
    v = np.cross(a,b)
    s = np.linalg.norm(v) 
    if not np.allclose(s, 0):
        c = np.dot(a,b)
        vskew = np.array([[0, -v[2], v[1]], [v[2], 0 , -v[0]], [-v[1], v[0], 0]  ])
        # rotation matrix rotating a into b
        R = np.eye(3) + vskew + np.dot(vskew, vskew) * ((1-c)/(s**2))
    else:
        R = np.eye(3)
    assert np.allclose(R.dot(a), b)
    # components are not in the right order 
    qi = Quaternion(matrix=R).elements
    return np.array([qi[1], qi[2], qi[3], qi[0]])

def getCoordPointsAlongHellix(r, layangle, npt, tmax, c = 1):
    x = np.zeros((npt,3), dtype = float)
    # field of tangent vectors
    xp = np.zeros((npt,3), dtype = float)
    t = np.linspace(0,tmax, npt)
    # Bussolati thesis --> eq. 2.2
    x[:,0] = r * np.cos(t)
    x[:,1] = r * np.sin(t)
    x[:,2] = r * (np.cos(layangle)/np.sin(layangle)) * t
    # import pdb; pdb.set_trace()

    xp[:,0] = -r * np.sin(t)
    xp[:,1] = r * np.cos(t)
    xp[:,2] = r * (np.cos(layangle)/np.sin(layangle)) 

    # https://math.stackexchange.com/a/476311/392320
    q = np.zeros((npt,4), dtype = float)
    a = np.array([1,0,0])
    # from this link, it looks like we need to provide the unit tangent vectors to the curve
    for i in range(npt):
        #tangent to the curve at the node
        b = xp[i]/np.linalg.norm(xp[i])
        q[i] = getOrientationQuaternion(a, b) 

    return x, q

class BeamFEMForceField (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):
        self.rootNode = rootNode
        UL = 1E-3
        lengthStrand = 1000 * UL  
        r= 1 
        E=100e9
        nu = 0.3
        nn = 25
        assert nn > 1
        nbeam = nn - 1
        # take gravity into account
        gravity = 0
        showCollisionModels = 0

        BC = 'AxialForceAtTip'
        indexNodeBC = nn-1
        DirectoryResults='./Tensile/'
        self.DirectoryResults = DirectoryResults
        if not os.path.exists(DirectoryResults):
            os.mkdir(DirectoryResults)

        dir_name = DirectoryResults 
        test = os.listdir(dir_name)
        for item in test:
            if item.endswith(".txt") or item.endswith(".vtu"):
                os.remove(os.path.join(dir_name, item))

        self.rootNode = rootNode
        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SofaExporter')
        rootNode.createObject('RequiredPlugin', name='SofaValidation')

        if showCollisionModels:
            rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        else:
            rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')

        if gravity:
            rootNode.gravity = [0,0,-9.81]
        else:
            rootNode.gravity = [0,0,0]

        # rootNode.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        rootNode.createObject('StaticSolver', newton_iterations=100,
            correction_tolerance_threshold='1.0e-9', residual_tolerance_threshold='1.0e-9',
            should_diverge_when_residual_is_growing=1)
        rootNode.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='1000')
        # topology
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        lines = lines.flatten().tolist()

        # rootNode/CentralBeam --> straight beam
        # x, q = getCoordPointsAlongHellix(0, np.deg2rad(0), nn, tmax = 2 * np.pi, c = p)
        number_dofs_per_node = 7

        if BC == 'AxialForceAtTip':
            #index of the last node
            forceApplied = [0, 0, 10000, 0, 0, 0]
        elif BC == 'MoveNodeAtTip':
            raise NotImplementedError

        Coord = np.zeros((nn, number_dofs_per_node),dtype=float)
        Coord[:, 2] = np.linspace(0, lengthStrand ,nn) 
        a = np.array([1,0,0])
        q = getOrientationQuaternion(a, np.array([0,0,1]))
        Coord[:, 3:] = q
        d = {"lengthStrand": lengthStrand}
        save_obj(d, DirectoryResults + 'infoSimu' )
        # strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        CentralBeam = rootNode.createChild('CentralBeam')
        self.CentralBeam = CentralBeam
        CentralBeam.createObject('MeshTopology', lines=lines, name='lines')
        CentralBeam.createObject('MechanicalObject', position= Coord.flatten().tolist(), name='DOFs', template='Rigid3d', showObject=0)
        CentralBeam.createObject('FixedConstraint', indices='0', name='FixedConstraint')
        CentralBeam.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false', showAxisSizeFactor=0)
        CentralBeam.createObject('BeamFEMForceField', radius=r, name='FEM', poissonRatio=nu, youngModulus=E)
        Collision = CentralBeam.createChild('Collision')
        self.Collision = Collision

        CentralBeam.createObject('ConstantForceField', indices=indexNodeBC, showArrowSize='0.0005', printLog='1', forces=forceApplied)

        CentralBeam.createObject('Monitor', name="DisplacementEndNode", indices=indexNodeBC,
        template="Rigid3d", showPositions=0, PositionsColor="1 0 1 1", ExportPositions=1 ,
        showVelocities=False, VelocitiesColor="0.5 0.5 1 1", ExportVelocities=False,
        showForces=0, ForcesColor="0.8 0.2 0.2 1", ExportForces=0, showTrajectories=0,
        TrajectoriesPrecision="0.1", TrajectoriesColor="0 1 1 1", sizeFactor="1",
        fileName=DirectoryResults + 'CentralBeamDisplacementEnd')

        self.endLoadingTime = 1

        self.reacForce = [] 

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
        t = self.rootNode.time
        print "t=" + str(t) +  "\n"

        beamC = self.rootNode.getChild('CentralBeam').getObject('FEM')
        fintC = np.array(beamC.getDataFields()['fintAllBeams'])[0]
        self.reacForce.append(np.array(fintC))

        if t > self.endLoadingTime:
            print "End of the loading reached. Post process starts"
            self.rootNode.animate = False
            np.savetxt(self.DirectoryResults + "ReactionForces.txt", np.array(self.reacForce))

            quit()

        
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
        # nodeBlocked = self.rootNode.getChild('CentralBeam').getObject('FixedConstraint').findData('indices').value
        # print 'node blocked is ' + str(nodeBlocked)
        # import pdb; pdb.set_trace()
        return 0;

def createScene(rootNode):
    rootNode.findData('dt').value = '0.1'
    rootNode.findData('gravity').value = '0 0 -9.81'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myBeamFEMForceField = BeamFEMForceField(rootNode,commandLineArguments)
    return 0;
