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
        UL = 1E-3
        # pitch length
        p = 115 * UL
        # heigth of the strand 
        h = p 
        layAngle = 11.8 # --> 90 - 72.8 where 72.8 is given by Jiang in his paper
        # radius of the core wire 
        # found in the paper of Jiang 1999
        # careful because the diameter is given, not the radius
        rCore = 0.5 * 3.93 * UL
        rHelli = 0.5 * 3.73 * UL
        radiusSphereCollisionModelCore = rCore 
        radiusSphereCollisionModelHeli = rHelli
        # Young's modulus
        E=188e9
        # Poisson's ratio
        nu = 0.3
        # parameter that control how many pitch length we have in the rope
        npitch = 2
        tmax = 0.5 * npitch * np.pi
        # number of nodes
        nn = npitch * int(self.commandLineArguments[1])
        assert nn > 1
        nbeam = nn - 1
        # target strand strain
        epsilon = 0.01 
        # take gravity into account
        gravity = 0
        BC = ['AxialForceAtTip', 'MoveNodeAtTip'][1]
        indexNodeBC = str(nn-1)
        DirectoryResults='./Tensile/'
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

        showCollisionModels = 0
        if showCollisionModels:
            rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields showCollisionModels')
        else:
            rootNode.createObject('VisualStyle', displayFlags='showBehaviorModels showForceFields')

        # rootNode.createObject('DefaultPipeline', draw='0', depth='6', verbose='0')
        # rootNode.createObject('BruteForceDetection', name='N2')
        # rootNode.createObject('MinProximityIntersection', contactDistance= 0.001 * UL, alarmDistance= 0.01 * UL, name='Proximity')
        # rootNode.createObject('DefaultContactManager', name='Response', response='default')

        if gravity:
            rootNode.gravity = [0,0,-9.81]
        else:
            rootNode.gravity = [0,0,0]

        rootNode.dt = 0.005
        rootNode.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
        rootNode.createObject('CGLinearSolver', threshold='1.0e-9', tolerance='1.0e-9', name='linear solver', iterations='25')

        # topology
        lines = np.zeros((nbeam, 2), dtype=int) 
        lines[:,0] = np.arange(0, nn -1)
        lines[:,1] = np.arange(1, nn)
        lines = lines.flatten().tolist()

        # rootNode/CentralBeam --> straight beam
        # x, q = getCoordPointsAlongHellix(0, np.deg2rad(0), nn, tmax = 2 * np.pi, c = p)
        number_dofs_per_node = 7

        # rootNode/beamJ --> helicoidal beam
        nHelix = 6
        rotAngle = 360/nHelix
        x, q = getCoordPointsAlongHellix( 1.1 * (rCore+rHelli), np.rad2deg(layAngle), nn, tmax = tmax, c = p)
        Coord = np.zeros((nn, number_dofs_per_node),dtype=float)
        Coord[:,:3] = x 
        Coord[:, 3:] = q
        lengthStrand = x[-1, 2] - x[0, 2]

        if BC == 'AxialForceAtTip':
            #index of the last node
            forceApplied = [0, 0, 10000, 0, 0, 0]
        elif BC == 'MoveNodeAtTip':
            index = str(nn-1)
            # easy to retrieve the displacement
            disp = epsilon * lengthStrand 
            keyTimes = np.zeros(3)
            self.endLoadingTime = 1
            keyTimes[0] = 0 
            keyTimes[1] = self.endLoadingTime 
            keyTimes[2] = 2*self.endLoadingTime 
            movements = np.zeros((keyTimes.shape[0], 6), dtype=float)
            movements[1] = [0, 0, disp, 0, 0, 0]
            movements[2] = [0, 0, disp, 0, 0, 0]
            keyTimes = keyTimes.ravel().tolist()
            movements = movements.ravel().tolist()

        for i in range(nHelix):
            strbeam = 'HellicalBeam' + str(i) 
            HeliBeami = rootNode.createChild(strbeam)
            setattr(self, strbeam, HeliBeami)
            # HeliBeami.createObject('EulerImplicitSolver', rayleighStiffness='0', printLog='false', rayleighMass='0.1')
            # HeliBeami.createObject('BTDLinearSolver', printLog='false', template='BTDMatrix6d', verbose='false')
            rot = "0 0 " + str(i * rotAngle)
            HeliBeami.createObject('MechanicalObject', position=Coord.flatten().tolist(), name='DOFs' + str(i), template='Rigid3d', rotation=rot)
            HeliBeami.createObject('MeshTopology', lines=lines, name='lines')
            HeliBeami.createObject('FixedConstraint', indices='0', name='FixedConstraint')
            HeliBeami.createObject('UniformMass', vertexMass='1 1 0.01 0 0 0 0.1 0 0 0 0.1', printLog='false',  showAxisSizeFactor=0)
            HeliBeami.createObject('BeamFEMForceField', radius=rHelli, name='FEM', poissonRatio=nu, youngModulus=E)
            HeliBeami.createObject('SphereModel', radius=radiusSphereCollisionModelHeli, name='SphereCollision'+str(i))
            index = str(nn-1)
            if BC == 'AxialForceAtTip':
                HeliBeami.createObject('ConstantForceField', indices=indexNodeBC, showArrowSize='0.0005', printLog='1', forces=forceApplied)
            elif BC == 'MoveNodeAtTip':
                HeliBeami.createObject('LinearMovementConstraint', keyTimes=keyTimes, template='Rigid3d', movements=movements, indices=indexNodeBC)

            HeliBeami.createObject('Monitor', name="ReactionForce" + strbeam, indices=0,
            template="Rigid3d", showPositions=0, PositionsColor="1 0 1 1", ExportPositions=False,
            showVelocities=False, VelocitiesColor="0.5 0.5 1 1", ExportVelocities=False,
            showForces=0, ForcesColor="0.8 0.2 0.2 1", ExportForces=True, showTrajectories=0,
            TrajectoriesPrecision="0.1", TrajectoriesColor="0 1 1 1", sizeFactor="1",
            fileName=DirectoryResults + strbeam + 'ReactionForce')
            

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
        CentralBeam.createObject('BeamFEMForceField', radius=rCore, name='FEM', poissonRatio=nu, youngModulus=E)
        Collision = CentralBeam.createChild('Collision')
        self.Collision = Collision

        CentralBeam.createObject('SphereModel', radius=radiusSphereCollisionModelCore, name='SphereCollision'+str(i+1))
        if BC == 'AxialForceAtTip':
            CentralBeam.createObject('ConstantForceField', indices=indexNodeBC, showArrowSize='0.0005', printLog='1', forces=forceApplied)
        elif BC == 'MoveNodeAtTip':
            CentralBeam.createObject('LinearMovementConstraint', keyTimes=keyTimes, template='Rigid3d', movements=movements, indices=indexNodeBC)

        CentralBeam.createObject('Monitor', name="ReactionForceCentralBeam", indices='0',
        template="Rigid3d", showPositions=0, PositionsColor="1 0 1 1", ExportPositions=False,
        showVelocities=False, VelocitiesColor="0.5 0.5 1 1", ExportVelocities=False,
        showForces=0, ForcesColor="0.8 0.2 0.2 1", ExportForces=True, showTrajectories=0,
        TrajectoriesPrecision="0.1", TrajectoriesColor="0 1 1 1", sizeFactor="1",
        fileName=DirectoryResults + 'CentralBeamReactionForce')

        CentralBeam.createObject('Monitor', name="DisplacementEndNode", indices=indexNodeBC,
        template="Rigid3d", showPositions=0, PositionsColor="1 0 1 1", ExportPositions=1 ,
        showVelocities=False, VelocitiesColor="0.5 0.5 1 1", ExportVelocities=False,
        showForces=0, ForcesColor="0.8 0.2 0.2 1", ExportForces=0, showTrajectories=0,
        TrajectoriesPrecision="0.1", TrajectoriesColor="0 1 1 1", sizeFactor="1",
        fileName=DirectoryResults + 'CentralBeamDisplacementEnd')



        HeliBeami.createObject(
            'VTKExporter',
            position="@DOFs"+str(i)+".position",
            edges="1",
            tetras="0",
            filename=DirectoryResults + "_frame_",
            exportEveryNumberOfSteps=1,
            listening=True)

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
        if t > self.endLoadingTime:
            print "End of the loading reached. Post process starts"
            self.rootNode.animate = False
            print("Force in an hellical beam")
            print(self.rootNode.HellicalBeam1.DOFs1.force[0])
            print("Force in central beam")
            print(self.rootNode.CentralBeam.DOFs.force[0])
            print("Reaction force at one end of the strand")
            RF0 = 6 * np.array(self.rootNode.HellicalBeam1.DOFs1.force[0]) + np.array(self.rootNode.CentralBeam.DOFs.force[0])
            print(RF0)
            print("Reaction force at the other end of the strand")
            RF00 = 6 * np.array(self.rootNode.HellicalBeam1.DOFs1.force[-1]) + np.array(self.rootNode.CentralBeam.DOFs.force[-1])
            print(RF00)
            import pdb; pdb.set_trace()
            quit()

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
        # nodeBlocked = self.rootNode.getChild('CentralBeam').getObject('FixedConstraint').findData('indices').value
        # print 'node blocked is ' + str(nodeBlocked)
        # import pdb; pdb.set_trace()
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
