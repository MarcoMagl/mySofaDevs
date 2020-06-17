import sys
import Sofa
import pickle
import numpy as np
import gmsh

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Cyl (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        FileMshBase="cylinder.msh"

        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 1)
        gmsh.open(FileMshBase)

        entities = gmsh.model.getEntities()
        FaceFixedFound = 0
        FacePulledFound= 0 
        import numpy as np

        for e in entities:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(dim, tag)

            # * Type and name of the entity:
            type = gmsh.model.getType(e[0], e[1])
            name = gmsh.model.getEntityName(e[0], e[1])
            if len(name): name += ' '
            print("Entity " + name + str(e) + " of type " + type)

            physicalTags = gmsh.model.getPhysicalGroupsForEntity(dim, tag)
            if len(physicalTags):
                for p in physicalTags:
                    n = gmsh.model.getPhysicalName(dim, p)
                    if n: n += ' '
                    if n == "FaceFixed ":
                        print "\n" + "FaceFixed found" + "\n"
                        FaceFixedFound = 1
                        idsBlockedNodes=np.array(nodeTags)
                        np.savetxt("nodesFaceFixed.txt", idsBlockedNodes ,fmt="%d")
                    elif n == "FacePulled ":
                        print "\n" + "FacePulled found" + "\n"
                        idsMovingNodes=np.array(nodeTags)
                        np.savetxt("nodesFacePulled.txt", idsMovingNodes, fmt="%d")
                        FacePulledFound = 1
                    
        assert FaceFixedFound and FacePulledFound, "Faces were not found"
        # We can use this to clear all the model data:
        gmsh.clear()
        gmsh.finalize()


        a_file = open("cylinder.msh", "r")
        lines = a_file.readlines()
        a_file.close()

        nlines = len(lines)
        i = 0
        linesToDel = []
        content = []
        
        while i < nlines:
            if "$PhysicalNames" in lines[i]:
                while not "$EndPhysicalNames" in lines[i]:
                    linesToDel.append(i)
                    content.append(lines[i])
                    i += 1
                linesToDel.append(i)
                content.append(lines[i])
                break
            i+=1

        for l in linesToDel:
            print(lines[l])

        del lines[linesToDel[0]:linesToDel[-1]+1]

        FileMsh=FileMshBase.split('.')[0] + "NoHead.msh"
        new_file = open(FileMsh, "w+")
        for line in lines:
            new_file.write(line)

        new_file.close()

        self.rootNode = rootNode
        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', name='SofaExporter')
        rootNode.createObject('VisualStyle', displayFlags='showForceFields')
        E = 188E3
        nu=0.33

        Wire = rootNode.createChild('Wire')
        self.Wire= Wire
        Wire.gravity = '0 0 0'

        Wire.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
        Wire.createObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='100') #, template='GraphScattered')
        Wire.createObject('MeshGmshLoader', name='meshLoader0', filename=FileMsh)
        Wire.createObject('MeshTopology', src='@meshLoader0', name='Topo')
        Wire.createObject('MechanicalObject', name='dofs', template='Vec3d')
        Wire.createObject('TetrahedronFEMForceField', template='Vec3d', youngModulus=E, poissonRatio=nu)
        Wire.createObject('UniformMass', name='mass', template='Vec3d', totalMass='0.5')
        import numpy as np
        idsBlockedNodes=(np.loadtxt("nodesFaceFixed.txt").astype(int) -1) .tolist()
        idsMovingdNodes=(np.loadtxt("nodesFacePulled.txt").astype(int)-1).tolist()

        print("\n Ids of nodes blocked" )
        print(idsBlockedNodes)
        print("\n Ids of nodes Pulled" )
        print(idsMovingdNodes)

        Wire.createObject('FixedConstraint', indices=idsBlockedNodes, name='HomogeneousBCs', template='Vec3d')

        disp = 10 
        self.endTime = 5 
        keyTimes = np.zeros(3)
        keyTimes[0] = 0 
        keyTimes[1] = 0 
        keyTimes[2] = self.endTime 
        movements = np.zeros((keyTimes.shape[0], 6), dtype=float)
        movements[0] = [0, 0, 0, 0, 0, 0]
        movements[1] = [0, 0, disp, 0, 0, 0]
        movements[2] = [0, 0, disp, 0, 0, 0]
        Wire.createObject('LinearMovementConstraint', keyTimes=keyTimes.ravel().tolist(), template='Vec3d', movements=movements.ravel().tolist(), indices=idsMovingdNodes) 

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
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
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
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def cleanup(self):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onGUIEvent(self, strControlID,valueName,strValue):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        t = self.rootNode.time
        print "t="
        print str(t)
        print "\n"
        if t > self.endTime: 
            import numpy as np
            self.rootNode.animate = False
            self.cleanup()
            # quit()
        
        return 0;

    def onLoaded(self, node):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def reset(self):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonMiddle(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Middle mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def bwdInitGraph(self, node):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onScriptEvent(self, senderNode, eventName,data):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;

    def onMouseButtonRight(self, mouseX,mouseY,isPressed):
        ## usage e.g.
        #if isPressed : 
        #    print "Control+Right mouse button pressed at position "+str(mouseX)+", "+str(mouseY)
        return 0;

    def onBeginAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /home/marcomag/WireModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        return 0;


def createScene(rootNode):
    rootNode.findData('dt').value = 0.05
    rootNode.findData('gravity').value = '0 -9.81 0'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myCyl = Cyl(rootNode,commandLineArguments)
    return 0;
