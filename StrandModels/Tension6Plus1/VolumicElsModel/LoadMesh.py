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
            assert useTets == 0 or  useTets == 1
        else:
            print("TOPOLOGY NOT PROVIDED. USING TETS TOPOLOGY BY DEFAULT\n")
            useTets = 1 #default

        # rootNode
        self.rootNode = rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SofaExporter')
        rootNode.createObject('RequiredPlugin', name='SofaSparseSolver')

        rootNode.createObject('VisualStyle', displayFlags='showForceFields')
        rootNode.createObject(
            'DefaultPipeline',
            name='CollisionPipeline',
            verbose='0')
        rootNode.createObject('BruteForceDetection', name='N2')
        rootNode.createObject(
            'DefaultContactManager',
            name='collision response',
            response='default')
        rootNode.createObject(
            'MinProximityIntersection',
            contactDistance=1e-3,
            alarmDistance=0.1,
            name='Proximity')


        a_file = open(FileMsh, "r")
        lines = a_file.readlines()
        a_file.close()

        nlines = len(lines)
        i = 0
        linesToDel = []
        content = []
        found = 0

        while i < nlines:
            if "$PhysicalNames" in lines[i]:
                found = 1
                while "$EndPhysicalNames" not in lines[i]:
                    linesToDel.append(i)
                    content.append(lines[i])
                    i += 1
                linesToDel.append(i)
                content.append(lines[i])
                break
            i += 1

        if found:
            for l in linesToDel:
                print(lines[l])

            del lines[linesToDel[0]:linesToDel[-1] + 1]

        baseName = FileMsh.split('.')[0]

        FileMshNoHead = baseName + "NoHead.msh"
        new_file = open(FileMshNoHead, "w+")
        for line in lines:
            new_file.write(line)

        new_file.close()

        # rootNode/LiverTriangles
        Strand = rootNode.createChild('Strand')
        self.Strand = Strand
        # Strand.depend = 'topo dofs'
        # careful with the unit --> 9.81 m.s-2 = 9.81 * 1e3 mm.s-2
        Strand.gravity = [0, -9.81 * 1e3, 0]

        # Strand.createObject('StaticSolver')
        Strand.createObject(
            'EulerImplicitSolver',
            printLog='0',
            rayleighStiffness='0.1',
            name='cg_odesolver',
            rayleighMass='0.1')
        Strand.createObject(
            'CGLinearSolver',
            threshold='1e-09',
            tolerance='1e-09',
            name='linear solver',
            iterations='50',
            template='GraphScattered')
        Strand.createObject(
            'MeshGmshLoader',
            name='meshLoader0',
            filename=FileMshNoHead)
        Strand.createObject('MeshTopology', src='@meshLoader0', name='Topo')
        Strand.createObject('MechanicalObject', name='dofs', template='Vec3d')

        E = 10
        nu = 0.3
        if useTets:
            Strand.createObject(
                'TetrahedronFEMForceField',
                template='Vec3d',
                youngModulus=E,
                poissonRatio=nu)
        else:
            # --> And not HexahedralFEMForceField!
            Strand.createObject(
                'HexahedronFEMForceField',
                template='Vec3d',
                youngModulus=E,
                poissonRatio=nu,
                method="large")


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
        if t > self.endTime:
            import numpy as np
            print "End of the loading reached. Post process starts"
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
        return 0


def createScene(rootNode):
    rootNode.findData('dt').value = '0.1'
    rootNode.findData('gravity').value = '0 -9.81 0'
    try:
        sys.argv[0]
    except BaseException:
        commandLineArguments = []
    else:
        commandLineArguments = sys.argv
    mystrand = strand(rootNode, commandLineArguments)
    return 0
