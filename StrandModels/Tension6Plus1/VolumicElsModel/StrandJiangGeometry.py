import sys
import Sofa
import pickle
import numpy as np
import gmsh


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


class strand (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments):
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : " + \
            str(commandLineArguments)
        self.createGraph(node)
        return None

    def createGraph(self, rootNode):

        FileMsh = self.commandLineArguments[1]
        if len(self.commandLineArguments) > 2:
            useTets = int(self.commandLineArguments[2])
            assert useTets == 0 or  useTets == 1, "Expecting a boolean for the second argument provided by --argv"
        else:
            raise ValueError("It is not indicated if tetrahedron or hexahedron have to be used")

        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.open(FileMsh)

        entities = gmsh.model.getEntities()
        FaceFixedFound = 0
        FacePulledFound = 0
        import numpy as np
        idsBlockedNodes = []
        idsMovingNodes = []

        for e in entities:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(
                dim, tag)

            # * Type and name of the entity:
            type = gmsh.model.getType(e[0], e[1])
            name = gmsh.model.getEntityName(e[0], e[1])
            if len(name):
                name += ' '
            print("Entity " + name + str(e) + " of type " + type)

            physicalTags = gmsh.model.getPhysicalGroupsForEntity(dim, tag)
            if len(physicalTags):
                for p in physicalTags:
                    n = gmsh.model.getPhysicalName(dim, p)
                    if n:
                        n += ' '
                    if n == "FaceFixed ":
                        print "\n" + "FaceFixed found" + "\n"
                        FaceFixedFound = 1
                        idsBlockedNodes.append(np.array(nodeTags))
                    elif n == "FacePulled ":
                        print "\n" + "FacePulled found" + "\n"
                        idsMovingNodes.append(np.array(nodeTags))
                        FacePulledFound = 1

        assert FaceFixedFound and FacePulledFound, "Faces were not found"
        # We can use this to clear all the model data:
        gmsh.clear()
        gmsh.finalize()

        idsBlockedNodes = (
            np.concatenate(idsBlockedNodes).astype(int).ravel() -
            1).tolist()
        idsMovingNodes = (
            np.concatenate(idsMovingNodes).astype(int).ravel() -
            1).tolist()
        self.idsBlockedNodes = idsBlockedNodes
        self.idsMovingNodes = idsMovingNodes

        print("\n Ids of nodes blocked:")
        print(idsBlockedNodes)
        print("\n Ids of nodes Pulled:")
        print(idsMovingNodes)

        a_file = open(FileMsh, "r")
        lines = a_file.readlines()
        a_file.close()

        nlines = len(lines)
        i = 0
        linesToDel = []
        content = []

        while i < nlines:
            if "$PhysicalNames" in lines[i]:
                while "$EndPhysicalNames" not in lines[i]:
                    linesToDel.append(i)
                    content.append(lines[i])
                    i += 1
                linesToDel.append(i)
                content.append(lines[i])
                break
            i += 1

        for l in linesToDel:
            print(lines[l])

        del lines[linesToDel[0]:linesToDel[-1] + 1]

        baseName = FileMsh.split('.')[0]
        FileMshNoHead = baseName + "NoHead.msh"
        new_file = open(FileMshNoHead, "w+")
        for line in lines:
            new_file.write(line)

        new_file.close()

        self.DirectoryResults = './' + baseName + '/'
        DirectoryResults = self.DirectoryResults
        import os
        self.DirectoryResults = DirectoryResults
        if not os.path.exists(DirectoryResults):
            os.mkdir(DirectoryResults)
        else:
            from os import listdir
            test = os.listdir(DirectoryResults)
            for item in test:
                try:
                    if item.endswith(".txt") or item.endswith(".vtu"):
                        os.remove(DirectoryResults + item)
                except BaseException:
                    import pdb
                    pdb.set_trace()

        # rootNode
        self.rootNode = rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SofaExporter')
        rootNode.createObject('RequiredPlugin', name='SofaSparseSolver')
        rootNode.createObject('RequiredPlugin', name='SofaMiscCollision')

        rootNode.createObject('VisualStyle', displayFlags='showForceFields')

        # rootNode.createObject(
        #     'DefaultPipeline',
        #     name='CollisionPipeline',
        #     verbose='0')
        # rootNode.createObject('BruteForceDetection', name='N2')
        # rootNode.createObject(
        #     'DefaultContactManager',
        #     name='collision response',
        #     response='default')
        # rootNode.createObject(
        #     'MinProximityIntersection',
        #     contactDistance=1e-3,
        #     alarmDistance=0.1,
        #     name='Proximity')

        rootNode.createObject('DefaultPipeline', draw='0', depth='10', verbose='0')
        rootNode.createObject('RayTraceDetection', name='N2')
        rootNode.createObject('NewProximityIntersection', contactDistance='0.7', alarmDistance='2', name='Proximity')
        rootNode.createObject('DefaultContactManager', name='Response', response='default')
        rootNode.createObject('DefaultCollisionGroupManager', name='Group')

        # be careful! We work in m ! --> FreeCAD works by default in mm.
        # No way to change this. So in the .geo files produced by gmsh one has to 
        # write Mesh.ScalingFactor=0.001 to have the nodes position in mm
        UL = 1E-3
        lengthStrand = 115 * UL
        E = 188E9
        nu = 0.3

        d = {"lengthStrand": lengthStrand,
             "DirectoryResults": DirectoryResults, 
             "nnodesBlocked": len(self.idsMovingNodes)}
        save_obj(d, DirectoryResults + 'infoSimu')

        # rootNode/LiverTriangles
        Strand = rootNode.createChild('Strand')
        self.Strand = Strand
        Strand.gravity = [0, -9.81, 0]

        Strand.createObject('StaticSolver', newton_iterations=100,
            correction_tolerance_threshold='1.0e-9', residual_tolerance_threshold='1.0e-9',
            should_diverge_when_residual_is_growing=1)
        # Strand.createObject(
        #     'EulerImplicitSolver',
        #     printLog='0',
        #     rayleighStiffness='0.1',
        #     name='cg_odesolver',
        #     rayleighMass='0.1')
        Strand.createObject(
            'CGLinearSolver',
            threshold='1e-09',
            tolerance='1e-09',
            name='linear solver',
            iterations='50',
            template='GraphScattered',
            verbose=0)
        Strand.createObject(
            'MeshGmshLoader',
            name='meshLoader0',
            filename=FileMshNoHead)
        Strand.createObject('MeshTopology', src='@meshLoader0', name='Topo')
        Strand.createObject('MechanicalObject', name='dofs', template='Vec3d')
        if useTets:
            Strand.createObject(
                'TetrahedronFEMForceField',
                template='Vec3d',
                youngModulus=E,
                poissonRatio=nu)
            Strand.createObject("TetrahedronSetGeometryAlgorithms", template="Vec3d")
        else:
            Strand.createObject(
                'HexahedronFEMForceField',
                template='Vec3d',
                youngModulus=E,
                poissonRatio=nu,
                method="large",
                updateStiffnessMatrix=1)
            Strand.createObject("HexahedronSetGeometryAlgorithms", template="Vec3d")
        Strand.createObject('MeshMatrixMass', name="Mass", lumping=1, massDensity='8100')
        # Strand.createObject(
        #     'UniformMass',
        #     name='mass',
        #     template='Vec3d',
        #     totalMass='0.5')


        Strand.createObject('TriangleCollisionModel', selfCollision=True)
        Strand.createObject('LineCollisionModel', selfCollision=True)
        Strand.createObject('PointCollisionModel', selfCollision=True)

        # HalfxBB = 8 * 0.5 * (rCore + rHelli)
        # HalfyBB = 8 * 0.5 * (rCore + rHelli)
        # HalfzBB=  2 * UL
        # Strand.createObject('BoxROI', box=[-HalfxBB, -HalfyBB, -HalfzBB, HalfxBB, HalfyBB, HalfzBB], drawBoxes='1', name='ROI1', computeTriangles='0', computeEdges='0', computeTetrahedra='0', template='Vec3d', position='@dofs.rest_position',
        # drawSize=0.1)
        # Strand.createObject('BoxROI', box=[-HalfxBB, -HalfyBB,  lengthStrand + -HalfzBB, HalfxBB, HalfyBB, lengthStrand + HalfzBB], drawBoxes='1', name='ROI2', computeTriangles='0', computeEdges='0', computeTetrahedra='0', template='Vec3d', position='@dofs.rest_position',
        # drawSize=0.1)

        keyTimes = np.zeros(3)
        movements = np.zeros((keyTimes.shape[0], 6), dtype=float)
        self.endTime = 1
        keyTimes[0] = 0
        keyTimes[1] = 0
        keyTimes[2] = self.endTime
        # target strand strain
        epsilon = 0.01
        # easy to retrieve the displacement
        disp = epsilon * lengthStrand

        Strand.createObject(
            'FixedConstraint',
            indices=idsBlockedNodes,
            name='HomogeneousBCs',
            template='Vec3d')
        movements[0] = [0, 0, 0, 0, 0, 0]
        movements[1] = [0, 0, disp, 0, 0, 0]
        movements[2] = [0, 0, disp, 0, 0, 0]
        Strand.createObject(
            'LinearMovementConstraint',
            keyTimes=keyTimes.ravel().tolist(),
            template='Vec3d',
            movements=movements.ravel().tolist(),
            indices=idsMovingNodes)
        # import pdb; pdb.set_trace()

        Strand.createObject(
            'Monitor',
            name="BlockedNodes_",
            indices=idsBlockedNodes,
            template="Vec3d",
            showPositions=0,
            ExportPositions=1,
            showForces=0,
            ExportForces=1,
            showTrajectories=0,
            sizeFactor="1",
            fileName=DirectoryResults +
            'MonitorBlockedNodes')

        Strand.createObject(
            'Monitor',
            name="MovingNodes_",
            indices=idsMovingNodes,
            template="Vec3d",
            showPositions=0,
            ExportPositions=1,
            showVelocities=False,
            ExportVelocities=False,
            showForces=0,
            ExportForces=1,
            showTrajectories=0,
            sizeFactor="1",
            fileName=DirectoryResults +
            'MonitorMovingNodes')

        # Strand.createObject('VTKExporter', position="@dofs.position", edges="1", tetras="1",
        # filename=baseName , exportEveryNumberOfSteps=1, exportAtEnd=1)

        # Strand.createObject(
        #     'VTKExporter',
        #     position="@dofs.position",
        #     edges="1",
        #     tetras="1",
        #     filename=DirectoryResults +
        #     baseName + "_frame_",
        #     exportEveryNumberOfSteps=1,
        #     listening=True)

        # self.rootnode.createObject("BarycentricShapeFunction")
        # self.rootnode.createObject(
        #     "TopologyGaussPointSampler",
        #     name="GaussPts",
        #     inPosition="@dofs.rest_position",
        #     tetrahedra="@topology.tetrahedra",
        #     showSamplesScale="0",
        #     order=1,
        # )

        return 0

    def onMouseButtonLeft(self, mouseX, mouseY, isPressed):
        # usage e.g.
        # if isPressed :
        #    print "Control+Left mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0

    def onKeyReleased(self, c):
        # usage e.g.
        # if c=="A" :
        #    print "You released a"
        return 0

    def initGraph(self, node):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onKeyPressed(self, c):
        # usage e.g.
        # if c=="A" :
        #    print "You pressed control+a"
        return 0

    def onMouseWheel(self, mouseX, mouseY, wheelDelta):
        # usage e.g.
        # if isPressed :
        #    print "Control button pressed+mouse wheel turned at position "+str(mouseX)+", "+str(mouseY)+", wheel delta"+str(wheelDelta)
        return 0

    def storeResetState(self):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def cleanup(self):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onGUIEvent(self, strControlID, valueName, strValue):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onEndAnimationStep(self, deltaTime):
        # Please feel free to add an example for a simple usage in
        # /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        t = self.rootNode.time

        print "t="
        print str(t)
        print "\n"

        # self.step += 1
        # import numpy as np
        # disp = np.array(self.Strand.dofs.position)[self.idsMovingNodes,] - self.initialPositionMovingNodes
        # self.disp_moving_nodes = np.vstack((self.disp_moving_nodes, disp.ravel()))

        if t > self.endTime:
            import numpy as np
            print "End of the loading reached. Post process starts"
            # np.save(self.DirectoryResults + 'disp_moving_nodes' , self.disp_moving_nodes)
            self.rootNode.animate = False
            self.cleanup()
            quit()

        return 0

    def onLoaded(self, node):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def reset(self):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onMouseButtonMiddle(self, mouseX, mouseY, isPressed):
        # usage e.g.
        # if isPressed :
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0

    def bwdInitGraph(self, node):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onScriptEvent(self, senderNode, eventName, data):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onMouseButtonRight(self, mouseX, mouseY, isPressed):
        # usage e.g.
        # if isPressed :
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0

    def onBeginAnimationStep(self, deltaTime):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        # if self.rootNode.time == 0:
        #     self.initialPositionMovingNodes = np.array(self.Strand.dofs.position)[self.idsMovingNodes,]
        #     # self.step = 0 
        #     self.disp_moving_nodes =  np.zeros(self.initialPositionMovingNodes.shape).ravel()
            # np.save(self.DirectoryResults + 'disp_moving_nodes_' + str(self.step), np.zeros(self.initialPositionMovingNodes.shape) )
        if self.rootNode.time == 0: 
            assert np.array(self.Strand.dofs.rest_position)[:,2].max() >= 0.115
        return 0


def createScene(rootNode):
    rootNode.findData('dt').value = '0.001'
    # rootNode.findData('gravity').value = '0 -9.81 0'
    try:
        sys.argv[0]
    except BaseException:
        commandLineArguments = []
    else:
        commandLineArguments = sys.argv
    mystrand = strand(rootNode, commandLineArguments)
    return 0
