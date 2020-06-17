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
    x[:,0] = r * np.cos(t)
    x[:,1] = r * np.sin(t)
    x[:,2] = r * (t/np.tan(layangle))
    # import pdb; pdb.set_trace()

    xp[:,0] = -r * np.sin(t)
    xp[:,1] = r * np.cos(t)
    xp[:,2] =  r/np.tan(layangle)

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

        UL = 1e-3
        rBeam = 3.* UL
        widthBB = 0.1 * UL
        E=100e9
        nu=0.33
        rootNode.gravity = '0 0 0'
        lengthBeam = 100*UL
        forceApplied = -1
        self.dictInfo = {"L":lengthBeam, "F": forceApplied, "E":E, "r":rBeam }

        # number of nodes
        nn = 100 
        assert nn > 1
        nbeam = nn - 1
        # take gravity into account
        gravity = 0
        BC = ['AxialForceAtTip', 'MoveNodeAtTip'][0]
        indexNodeBC = str(nn-1)
        DirectoryResults='./Cantilever/'
        self.DirectoryResults = DirectoryResults
        if not os.path.exists(DirectoryResults):
            os.mkdir(DirectoryResults)
        dir_name = DirectoryResults 
        test = os.listdir(dir_name)
        for item in test:
            if item.endswith(".txt"):
                os.remove(os.path.join(dir_name, item))

        self.rootNode = rootNode
        # rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SofaExporter')
        rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')

        if gravity:
            rootNode.gravity = [0,0,-9.81]
        else:
            rootNode.gravity = [0,0,0]

        rootNode.dt = 0.1
        static = 1

        if not static:
            rootNode.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
            self.solverType = "EulerImplicit"
        else:
            rootNode.createObject('StaticSolver', newton_iterations=100, correction_tolerance_threshold=1E-12,
            residual_tolerance_threshold=1e-12)

            self.solverType = "Static"
        rootNode.createObject('CholeskySolver')# , threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='25', template='GraphScattered')

        # topology
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        lines = lines.flatten().tolist()

        # rootNode/Beam --> straight beam
        # x, q = getCoordPointsAlongHellix(0, np.deg2rad(0), nn, tmax = 2 * np.pi, c = p)
        number_dofs_per_node = 7
        self.endLoadingTime = 1

        if BC == 'AxialForceAtTip':
            #index of the last node
            VforceApplied = [0, forceApplied, 0, 0, 0, 0]
        elif BC == 'MoveNodeAtTip':
            index = str(nn-1)
            # easy to retrieve the displacement
            disp = epsilon * lengthBeam
            keyTimes = np.zeros(3)
            keyTimes[0] = 0 
            keyTimes[1] = self.endLoadingTime 
            keyTimes[2] = 2*self.endLoadingTime 
            movements = np.zeros((keyTimes.shape[0], 6), dtype=float)
            movements[1] = [0, 0, disp, 0, 0, 0]
            movements[2] = [0, 0, disp, 0, 0, 0]
            keyTimes = keyTimes.ravel().tolist()
            movements = movements.ravel().tolist()

        Coord = np.zeros((nn, number_dofs_per_node),dtype=float)
        Coord[:, 2] = np.linspace(0, lengthBeam,nn) 
        a = np.array([1,0,0])
        q = getOrientationQuaternion(a, np.array([0,0,1]))
        Coord[:, 3:] = q
        # strCoord =  str(Coord.flatten()).replace('\n', '').replace('[', '').replace(']','')
        Beam = rootNode.createChild('Beam')
        self.Beam = Beam
        Beam.createObject('MeshTopology', lines=lines, name='lines')
        Beam.createObject('MechanicalObject', position= Coord.flatten().tolist(), name='DOFs', template='Rigid3d', showObject=0)
        Beam.createObject('FixedConstraint', indices=[0], name='FixedConstraint')
        Beam.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false', showAxisSizeFactor=0)
        Beam.createObject('BeamFEMForceField', radius=rBeam, name='FEM', poissonRatio=nu, youngModulus=E)
        Collision = Beam.createChild('Collision')
        self.Collision = Collision

        if BC == 'AxialForceAtTip':
            Beam.createObject('ConstantForceField', indices=indexNodeBC, showArrowSize='0.0000', printLog='0', totalForce=VforceApplied, topology="@lines")
        elif BC == 'MoveNodeAtTip':
            Beam.createObject('LinearMovementConstraint', keyTimes=keyTimes, template='Rigid3d', movements=movements, indices=indexNodeBC)

        # Beam.createObject('Monitor', name="ReactionForceBeam", indices='0',
        # template="Rigid3d", showPositions=0, PositionsColor="1 0 1 1", ExportPositions=False,
        # showVelocities=False, VelocitiesColor="0.5 0.5 1 1", ExportVelocities=False,
        # showForces=0, ForcesColor="0.8 0.2 0.2 1", ExportForces=True, showTrajectories=0,
        # TrajectoriesPrecision="0.1", TrajectoriesColor="0 1 1 1", sizeFactor="1",
        # fileName=DirectoryResults + 'BeamReactionForce')

        # Beam.createObject('Monitor', name="DisplacementEndNode", indices=indexNodeBC,
        # template="Rigid3d", showPositions=0, PositionsColor="1 0 1 1", ExportPositions=1 ,
        # showVelocities=False, VelocitiesColor="0.5 0.5 1 1", ExportVelocities=False,
        # showForces=0, ForcesColor="0.8 0.2 0.2 1", ExportForces=0, showTrajectories=0,
        # TrajectoriesPrecision="0.1", TrajectoriesColor="0 1 1 1", sizeFactor="1",
        # fileName=DirectoryResults + 'BeamDisplacementEnd')

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
        # Deflec = np.array(self.rootNode.Beam.DOFs.position[-1]) - np.array(self.rootNode.Beam.DOFs.rest_position[-1])[1]
        AllDeflec = (np.array(self.rootNode.Beam.DOFs.position) - np.array(self.rootNode.Beam.DOFs.rest_position))[:,1]
        x = np.array(self.rootNode.Beam.DOFs.rest_position)[:,2]

        # only one time step
        print("Results:") 
        E = self.dictInfo["E"]
        F = self.dictInfo["F"]
        L = self.dictInfo["L"]
        r = self.dictInfo["r"]
        I = (np.pi * r**4) / 4 
        DeflecAnalytical = ((F * x**2)*(3 * L - x)) / (6 *E * I)
        ReacForce = np.array(self.rootNode.Beam.DOFs.force[-1])

        import matplotlib.pylab as plt
        plt.plot(x , AllDeflec, label="deflection along beam")
        plt.plot(x, DeflecAnalytical, '--', label="analytical deflection" )
        plt.legend()
        ax=plt.gca()
        ax.set_xlabel("step number")
        ax.set_ylabel("deflection at the tip")
        plt.pause(0.1)
        plt.savefig("CantileverBeam"+self.solverType+"BeamElements")
        import pdb; pdb.set_trace()
        quit()
        raise ValueError('Loading ended')

        # import pdb; pdb.set_trace()
        
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
        nodeBlocked = self.rootNode.getChild('Beam').getObject('FixedConstraint').findData('indices').value
        print 'node blocked is ' + str(nodeBlocked)
        # import pdb; pdb.set_trace()
        if self.rootNode.time == 0:
            self.deflec = []
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
