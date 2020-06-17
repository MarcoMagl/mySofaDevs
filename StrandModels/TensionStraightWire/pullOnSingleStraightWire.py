import sys
import Sofa
import pickle
import gmsh


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


class TutorialForceFieldLiverTriangleFEM (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments):
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : " + \
            str(commandLineArguments)
        self.createGraph(node)
        return None

    def createGraph(self, rootNode):

        FileMsh = self.commandLineArguments[1]
        baseName = FileMsh.split('.')[0]
        self.DirectoryResults = './' + baseName + '/'
        DirectoryResults = self.DirectoryResults
        import os
        self.DirectoryResults = DirectoryResults
        if not os.path.exists(DirectoryResults):
            os.mkdir(DirectoryResults)

        files_in_directory = os.listdir(DirectoryResults)
        filtered_files = [
            file for file in files_in_directory if file.endswith(".txt")]

        for file in filtered_files:
            path_to_file = os.path.join(DirectoryResults, file)
            os.remove(path_to_file)

        FileMsh = self.commandLineArguments[1]
        if len(self.commandLineArguments) > 2:
            useTets = int(self.commandLineArguments[2])
            assert useTets == 0 or useTets == 1, "Expecting a boolean for the second argument provided by --argv"
        else:
            useTets = 1  # default

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
                    if n == "FaceBlocked":
                        print "\n" + "FaceFixed found" + "\n"
                        FaceFixedFound = 1
                        idsBlockedNodes.append(np.array(nodeTags))
                    elif n == "FacePulled":
                        print "\n" + "FacePulled found" + "\n"
                        idsMovingNodes.append(np.array(nodeTags))
                        FacePulledFound = 1

        idsBlockedNodes = (
            np.array(idsBlockedNodes).astype(int).ravel() -
            1).tolist()
        idsMovingNodes = (
            np.array(idsMovingNodes).astype(int).ravel() -
            1).tolist()
        self.idsBlockedNodes = idsBlockedNodes
        self.idsMovingNodes = idsMovingNodes

        assert FaceFixedFound and FacePulledFound, "Faces were not found"
        # We can use this to clear all the model data:
        gmsh.clear()
        gmsh.finalize()

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

        # rootNode
        self.rootNode = rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SofaExporter')
        rootNode.createObject('RequiredPlugin', name='SofaSparseSolver')

        rootNode.createObject('VisualStyle', displayFlags='showForceFields')
        # rootNode.createObject('DefaultPipeline', name='CollisionPipeline', verbose='0')
        # rootNode.createObject('BruteForceDetection', name='N2')
        # rootNode.createObject('DefaultContactManager', name='collision response', response='default')
        # rootNode.createObject('MinProximityIntersection', contactDistance=1e-3, alarmDistance=0.1, name='Proximity')

        # be careful! We work in mm !
        # this is because the geometry from Freecad is in mm by default
        UL = 1
        rCore = 0.5 * 3. * UL
        lengthWire = 100 * UL
        # https://www.translatorscafe.com/unit-converter/en-US/pressure/5-20/gigapascal-newton/millimeter%C2%B2/
        E = 188E3

        d = {"lengthWire": lengthWire, "DirectoryResults": DirectoryResults}
        save_obj(d, DirectoryResults + 'infoSimu')

        # rootNode/LiverTriangles
        Wire = rootNode.createChild('Wire')
        self.Wire = Wire
        Wire.gravity = '0 0 0'

        #Wire.createObject('StaticSolver', newton_iterations=10)
        Wire.createObject(
            'EulerImplicitSolver',
            printLog='0',
            rayleighStiffness='0.1',
            name='cg_odesolver',
            rayleighMass='0.1')
        Wire.createObject(
            'CGLinearSolver',
            threshold='1e-09',
            tolerance='1e-09',
            name='linear solver',
            iterations='100')  # , template='GraphScattered')
        Wire.createObject(
            'MeshGmshLoader',
            name='meshLoader0',
            filename=FileMshNoHead)
        Wire.createObject('MeshTopology', src='@meshLoader0', name='Topo')
        Wire.createObject('MechanicalObject', name='dofs', template='Vec3d')
        Wire.createObject(
            'TetrahedronFEMForceField',
            template='Vec3d',
            youngModulus=E,
            poissonRatio=0.33)
        Wire.createObject(
            'UniformMass',
            name='mass',
            template='Vec3d',
            totalMass='0.5')
        HalfxBB = 8 * 0.5 * (rCore)
        HalfyBB = 8 * 0.5 * (rCore)
        HalfzBB = 0.1 * UL
        self.MovingROI = Wire.createObject('BoxROI',
                                           box=[-HalfxBB,
                                                -HalfyBB,
                                                -HalfzBB,
                                                HalfxBB,
                                                HalfyBB,
                                                HalfzBB],
                                           drawBoxes='1',
                                           name='MovingROI',
                                           computeTriangles='0',
                                           computeEdges='0',
                                           computeTetrahedra='0',
                                           template='Vec3d',
                                           position='@dofs.rest_position',
                                           drawSize=0.1)

        self.FixedROI = Wire.createObject('BoxROI',
                                          box=[-HalfxBB,
                                               -HalfyBB,
                                               lengthWire + -HalfzBB,
                                               HalfxBB,
                                               HalfyBB,
                                               lengthWire + HalfzBB],
                                          drawBoxes='1',
                                          name='FixedROI',
                                          computeTriangles='0',
                                          computeEdges='0',
                                          computeTetrahedra='0',
                                          template='Vec3d',
                                          position='@dofs.rest_position',
                                          drawSize=0.1)

        import numpy as np
        # target Wire strain
        epsilon = 0.01
        # easy to retrieve the displacement
        disp = epsilon * lengthWire
        self.endTime = 1
        keyTimes = np.zeros(3)
        keyTimes[0] = 0
        keyTimes[1] = 0
        keyTimes[2] = self.endTime
        movements = np.zeros((keyTimes.shape[0], 6), dtype=float)
        # movements[0] = [0, 0, disp, 0, 0, 0]
        movements[0] = [0, 0, 0, 0, 0, 0]
        movements[1] = [0, 0, disp, 0, 0, 0]
        movements[2] = [0, 0, disp, 0, 0, 0]
        Wire.createObject(
            'FixedConstraint',
            indices='@FixedROI.indices',
            name='HomogeneousBCs',
            template='Vec3d')
        Wire.createObject(
            'LinearMovementConstraint',
            keyTimes=keyTimes.ravel().tolist(),
            template='Vec3d',
            movements=movements.ravel().tolist(),
            indices='@MovingROI.indices')
        # import pdb; pdb.set_trace()

        Wire.createObject(
            'Monitor',
            name="ReactionForceBlockedNodes",
            indices='@FixedROI.indices',
            template="Vec3d",
            showPositions=1,
            PositionsColor="115 210 22 255",
            ExportPositions=False,
            showVelocities=False,
            VelocitiesColor="0.5 0.5 1 1",
            ExportVelocities=False,
            showForces=1,
            ForcesColor="0.8 0.2 0.2 1",
            ExportForces=True,
            showTrajectories=0,
            TrajectoriesPrecision="0.1",
            TrajectoriesColor="0 1 1 1",
            sizeFactor=0.04,
            fileName=DirectoryResults +
            'ReactionForce')

        Wire.createObject(
            'Monitor',
            name="DisplacementEndNode",
            indices='@MovingROI.indices',
            template="Vec3d",
            showPositions=1,
            PositionsColor="1 0 1 1",
            ExportPositions=1,
            showVelocities=False,
            VelocitiesColor="0.5 0.5 1 1",
            ExportVelocities=False,
            showForces=0,
            ForcesColor="0.8 0.2 0.2 1",
            ExportForces=0,
            showTrajectories=0,
            TrajectoriesPrecision="0.1",
            TrajectoriesColor="0 1 1 1",
            sizeFactor=1,
            fileName=DirectoryResults +
            'CentralBeamDisplacementEnd')

        Wire.createObject(
            'Monitor',
            name="ReactionForceBlockedNodes2",
            indices=idsBlockedNodes,
            template="Vec3d",
            showPositions=1,
            PositionsColor="115 210 22 255",
            ExportPositions=False,
            showVelocities=False,
            VelocitiesColor="0.5 0.5 1 1",
            ExportVelocities=False,
            showForces=1,
            ForcesColor="0.8 0.2 0.2 1",
            ExportForces=True,
            showTrajectories=0,
            TrajectoriesPrecision="0.1",
            TrajectoriesColor="0 1 1 1",
            sizeFactor=0.04,
            fileName=DirectoryResults +
            'ReactionForce2WoROI')

        Wire.createObject(
            'Monitor',
            name="DisplacementEndNode2",
            indices=idsMovingNodes,
            template="Vec3d",
            showPositions=1,
            PositionsColor="1 0 1 1",
            ExportPositions=1,
            showVelocities=False,
            VelocitiesColor="0.5 0.5 1 1",
            ExportVelocities=False,
            showForces=0,
            ForcesColor="0.8 0.2 0.2 1",
            ExportForces=0,
            showTrajectories=0,
            TrajectoriesPrecision="0.1",
            TrajectoriesColor="0 1 1 1",
            sizeFactor=1,
            fileName=DirectoryResults +
            'CentralBeamDisplacementEndWoROI')
        # Wire.createObject('VTKExporter', position="@dofs.position", edges="1", tetras="1",
        # filename=baseName , exportEveryNumberOfSteps=1, listening=True)

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
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def cleanup(self):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onGUIEvent(self, strControlID, valueName, strValue):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onEndAnimationStep(self, deltaTime):
        # Please feel free to add an example for a simple usage in
        # /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        t = self.rootNode.time
        print "t="
        print str(t)
        print "\n"
        if t > self.endTime:
            import numpy as np
            print "End of the loading reached. Post process starts"
            self.rootNode.animate = False
            self.cleanup()
            quit()

        return 0

    def onLoaded(self, node):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def reset(self):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onMouseButtonMiddle(self, mouseX, mouseY, isPressed):
        # usage e.g.
        # if isPressed :
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0

    def bwdInitGraph(self, node):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onScriptEvent(self, senderNode, eventName, data):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0

    def onMouseButtonRight(self, mouseX, mouseY, isPressed):
        # usage e.g.
        # if isPressed :
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0

    def onBeginAnimationStep(self, deltaTime):
        # Please feel free to add an example for a simple usage in
        # /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        import numpy as np
        arr1 = np.array(self.MovingROI.indices).ravel()
        try:
            assert np.array_equal(arr1, self.idsMovingNodes)
        except AssertionError:
            import pdb
            pdb.set_trace()

        arr2 = np.array(self.FixedROI.indices).ravel()
        try:
            assert np.array_equal(arr2, self.idsBlockedNodes)
        except AssertionError:
            import pdb
            pdb.set_trace()

        return 0


def createScene(rootNode):
    rootNode.findData('dt').value = 0.1
    rootNode.findData('gravity').value = '0 -9.81 0'
    try:
        sys.argv[0]
    except BaseException:
        commandLineArguments = []
    else:
        commandLineArguments = sys.argv
    myTutorialForceFieldLiverTriangleFEM = TutorialForceFieldLiverTriangleFEM(
        rootNode, commandLineArguments)
    return 0
