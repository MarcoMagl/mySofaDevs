import sys
import Sofa
import numpy as np

class ClampedBeam (Sofa.PythonScriptController):

    def __init__(self, node, commandLineArguments) : 
        self.commandLineArguments = commandLineArguments
        print "Command line arguments for python : "+str(commandLineArguments)
        self.createGraph(node)
        return None;

    def createGraph(self,rootNode):

        rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')
        rootNode.createObject('RequiredPlugin', name='Flexible')
        rootNode.createObject('RequiredPlugin', name='SofaPython')
        rootNode.createObject('RequiredPlugin', pluginName='Compliant', name='Compliant')
        rootNode.createObject('VisualStyle', displayFlags="showVisualModels showBehaviorModels showForceFields")

        """
        material properties and geometry
        """
        UL = 1e-3
        rBeam = 3.* UL
        widthBB = 0.1 * UL
        E=100e9
        nu=0.33
        rootNode.gravity = '0 0 0'
        lengthBeam = 200*UL
        forceApplied = -1
        """
        material properties and geometry
        """

        """
        mesh and solver 
        """
        self.rootNode = rootNode
        rootNode.createObject('MeshGmshLoader', name='meshLoader0', filename='SingleStraightWire.msh')
        Beam = rootNode.createChild('Beam')
        self.Beam= Beam
        static = 1 
        if not static:
            Beam.createObject('EulerImplicitSolver', printLog='0', rayleighStiffness='0.1', name='cg_odesolver', rayleighMass='0.1')
            self.solverType = "EulerImplicit"
        else:
            Beam.createObject('StaticSolver', newton_iterations=100, correction_tolerance_threshold=1E-12,
            residual_tolerance_threshold=1e-12)
            self.solverType = "Static"
        #Beam.createObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='25', template='GraphScattered')
        Beam.createObject('CholeskySolver')# , threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='25', template='GraphScattered')
        # Beam.createObject('CGLinearSolver', threshold='1e-09', tolerance='1e-09', name='linear solver', iterations='100', template='GraphScattered')
        # Beam.createObject('MeshTopology', src='@meshLoader0', name='Topo')
        Beam.createObject('MechanicalObject', name='dofs', template='Vec3d', src='@../meshLoader0') #, position="@Topo.position")
        # Beam.createObject('TetrahedronSetTopologyContainer', src='@../meshLoader0', name='Topo')
        # Beam.createObject('TetrahedronSetGeometryAlgorithms')
        Beam.createObject("MeshTopology", name = "Topo", src = "@../meshLoader0")
        Beam.createObject('TetrahedronSetGeometryAlgorithms')
        """
        mesh and solver 
        """


        """
        BCs and material law
        """
        fancyMass = 1
        if not fancyMass:
            Beam.createObject('UniformMass', name='mass', template='Vec3d', totalMass='10')
        else:
            Beam.createObject('MeshMatrixMass', massDensity=9100, topology='@Topo')

        xmin = -1.1*rBeam
        ymin = float(xmin)
        zmin = -widthBB
        xmax = -xmin
        ymax = -ymin
        zmax = -zmin
        Beam.createObject('BoxROI', box=[xmin, ymin, zmin, xmax, ymax, zmax], drawBoxes='1', name='FixedROI', computeTriangles='0', computeEdges='0', computeTetrahedra='0', template='Vec3d', position='@dofs.rest_position',
        drawSize=0.1)
        Beam.createObject('FixedConstraint', indices='@FixedROI.indices', name='HomogeneousBCs', template='Vec3d')

        Beam.createObject('BoxROI', box=[xmin, ymin, zmin + lengthBeam, xmax , ymax, zmax + lengthBeam], drawBoxes='1', drawSize=0.1, name='NeumanROI', computeTriangles='0', computeEdges='0', computeTetrahedra='0', template='Vec3d', position='@dofs.rest_position')
        # waring ==> if we use the "force" keyword, the force prescribed is repeated over all the nodes !
        BC = "Neuman"

        self.endLoadingTime = 0.1
        if BC == "Neuman":
            Beam.createObject('ConstantForceField', indices='@NeumanROI.indices', showArrowSize='0.0000', printLog='0', totalForce=[0, forceApplied, 0], topology="@Topo")
        elif BC == "Dirichlet":
            disp = - 2 * UL
            keyTimes = np.zeros(3)
            keyTimes[0] = 0 
            keyTimes[1] = self.endLoadingTime 
            keyTimes[2] = 2*self.endLoadingTime 
            movements = np.zeros((keyTimes.shape[0], 3), dtype=float)
            movements[1] = [0, disp, 0]
            movements[2] = [0, disp, 0]
            keyTimes = keyTimes.ravel().tolist()
            movements = movements.ravel().tolist()
            Beam.createObject('LinearMovementConstraint', keyTimes=keyTimes, template='Vec3d', movements=movements, indices='@NeumanROI.indices')
        else:
            raise NotImplementedError


        fancyMaterialLaw = 0
        if fancyMaterialLaw:
            Beam.createObject("BarycentricShapeFunction")
            beh_node = Beam.createChild("behavior")
            beh_node.createObject(
                "TopologyGaussPointSampler",
                name="GaussPts",
                inPosition="@Topo.position",
                showSamplesScale="1.2", # to visualise the GP --> hide the FEMForceField
                order=1,
            )
            beh_node.createObject("MechanicalObject", template="F331", name="F", listening="True")
            beh_node.createObject("LinearMapping")

            u_node = beh_node.createChild("strain-stress")
            self.Mech2 = u_node.createObject("MechanicalObject", template="E331", name="U") # the template "E331" apparently corresponds to 3x3 matrices
            u_node.createObject('CorotationalStrainMapping', template="F331,E331", method="svd", assemble = 1)
            self.mat = u_node.createObject("HookeForceField", template="E331", youngModulus=E, poissonRatio=nu,)
        else                method="small",

            # fonctionne pas 
            Beam.createObject(
                'TetrahedronFEMForceField',
                template='Vec3d',
                youngModulus=E,
                poissonRatio=nu,
                topology="@Topo",
                updateStiffnessMatrix=1,
                computeGlobalMatrix=0,
                method="small",
                computeVonMisesStress=0,
                showStressColorMap="BlueToCyan",#"Red to Blue"
                plasticYieldThreshold=1.)
            # fonctionne mais c'est pas ce que je veux lol
            # Beam.createObject('TetrahedralCorotationalFEMForceField', method='large', template='Vec3d', name='FEM', poissonRatio='0.45', youngModulus='5000')
        """
        BCs and material law
        """

        # needed for post-processing
        self.dictInfo = {"L":lengthBeam, "F": forceApplied, "E":E, "r":rBeam }
        self.deflec = []
        return 0;

    def onEndAnimationStep(self, deltaTime):
        ## Please feel free to add an example for a simple usage in /home/marcomag/StrandModels//home/marcomag/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        # print self.Mech2.position 
        ## Please feel free to add an example for a simple usage in /Users/marco.magliulo/mySofaCodes/myScriptsToGetStarted//Users/marco.magliulo/Software/sofa/src/applications/plugins/SofaPython/scn2python.py
        t = self.rootNode.time
        print "t=" + str(t) +  "\n"
        nodeFollowed = self.idsClosestNodeFromCenter
        Deflec = np.array(self.rootNode.Beam.dofs.position[nodeFollowed]) - np.array(self.rootNode.Beam.dofs.rest_position[nodeFollowed])
        self.deflec.append(Deflec[1])
        if t > self.endLoadingTime:
            print("Results:") 
            E = self.dictInfo["E"]
            F = self.dictInfo["F"]
            L = self.dictInfo["L"]
            r = self.dictInfo["r"]
            I = (np.pi * r**4) * 0.25 
            DeflecAnalytical = (F * L**3) / (3 *E * I)
            import pdb; pdb.set_trace()
            ReacForce = np.array(self.rootNode.Beam.dofs.force[-1])
            import matplotlib.pylab as plt
            plt.plot(np.arange(len(self.deflec)), self.deflec, label="deflection of a node at the end")
            plt.plot(np.arange(len(self.deflec)), np.ones(len(self.deflec)) * DeflecAnalytical, '--', label="analytical deflection" )
            plt.legend()
            ax=plt.gca()
            ax.set_xlabel("step number")
            ax.set_ylabel("deflection at the tip")
            plt.pause(0.1)
            plt.savefig("CantileverBeamTetra"+self.solverType)
            # import pdb; pdb.set_trace()
            quit()
            raise ValueError('Loading ended')
        return 0;



    def onBeginAnimationStep(self, deltaTime):
        idsFaceBCs = np.array(self.rootNode.Beam.NeumanROI.indices).ravel()
        x = np.array(self.rootNode.Beam.dofs.rest_position)[idsFaceBCs,]
        L = self.dictInfo["L"]
        centerPt = np.array([0, 0, L])
        id_distMin = np.linalg.norm(x - centerPt, axis = 1).argmin()
        self.idsClosestNodeFromCenter = idsFaceBCs[id_distMin]



def createScene(rootNode):
    rootNode.findData('dt').value = '0.1'
    try : 
        sys.argv[0]
    except :
        commandLineArguments = []
    else :
        commandLineArguments = sys.argv
    myClampedBeam = ClampedBeam(rootNode,commandLineArguments)
    return 0;