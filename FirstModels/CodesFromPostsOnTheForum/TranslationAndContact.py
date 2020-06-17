import Sofa
import os

class MainScene(Sofa.PythonScriptController):

    def createGraph(self, node):

        dt = 0.01 # In second
        
        self.rootNode = node.getRoot()
        self.rootNode.dt = dt
        self.rootNode.gravity = [0, 0, 0]

        self.rootNode.createObject('APIVersion', name = 17.12)

        self.rootNode.createObject('RequiredPlugin', name='SofaMiscCollision')
        self.rootNode.createObject('RequiredPlugin', name='SofaPython')
        self.rootNode.createObject('RequiredPlugin', name='CImgPlugin')
        self.rootNode.createObject('RequiredPlugin', name='SofaOpenglVisual')

        self.rootNode.createObject('VisualStyle', displayFlags=['showBehaviorModels'])
        self.rootNode.createObject('FreeMotionAnimationLoop')
        
        self.rootNode.createObject('GenericConstraintSolver', maxIterations = 100, tolerance = 0.001)
        self.rootNode.createObject('DefaultPipeline', verbose='0', depth="6", draw='1')
        self.rootNode.createObject('BruteForceDetection', name = 'N2')
        self.rootNode.createObject("LocalMinDistance", name="Intersection", alarmDistance="0.3", contactDistance="0.1", useLMDFilters="0")
        self.rootNode.createObject('DefaultContactManager', name="Response", response="FrictionContact")

        #==========================
        # OBJECT
        #==========================
                        
        meshFile = "mesh/Armadillo_simplified.obj"
                    
        objectNode = self.rootNode.createChild("Armadillo")

        objectNode.createObject('EulerImplicitSolver', rayleighStiffness = 0.1, rayleighMass = 0.1)
        objectNode.createObject('CGLinearSolver', iterations=25, tolerance=1e-9, threshold=1e-9, printLog=True)
        objectNode.createObject('MechanicalObject', name = 'mechObject', 
                                                    dx="0", dy="0", dz="0", rx="0", ry="0", rz="0", scale="1.0")
        objectNode.createObject('UniformMass', totalMass="10")
                    
        objectNode.createObject('RegularGridTopology', nx = 7, ny = 8, nz = 6, 
                                                       xmin=-7, xmax=7, ymin=-6, ymax=10, zmin=-6, zmax=6)
        objectNode.createObject('RegularGridSpringForceField', name="Springs", stiffness="50", damping="1")
        objectNode.createObject('UncoupledConstraintCorrection')

        # Vis node
        objectVisNode = objectNode.createChild('Visu')
        objectVisNode.createObject('MeshObjLoader', name='meshLoader', filename = meshFile)
        objectVisNode.createObject('OglModel', src='@meshLoader')
        objectVisNode.createObject('BarycentricMapping')

        # Collision node
        objectSurfNode = objectNode.createChild('Surf')
        objectSurfNode.createObject('MeshObjLoader', name="meshLoader", filename = meshFile)
        objectSurfNode.createObject('MeshTopology', src="@meshLoader")
        objectSurfNode.createObject('MechanicalObject', src="@meshLoader", scale="1.0")
        objectSurfNode.createObject('TriangleCollisionModel')
        objectSurfNode.createObject('LineCollisionModel')
        objectSurfNode.createObject('PointCollisionModel')
        objectSurfNode.createObject('BarycentricMapping')


        # ==========================
        # INSTRUMENT
        # ==========================

        meshFile = "mesh/dental_instrument.obj"
        scale=2
        
        instrumentNode = self.rootNode.createChild("Instrument")

        instrumentNode.createObject('EulerImplicitSolver', name="ODE solver", rayleighStiffness="0.01", rayleighMass="1.0")
        instrumentNode.createObject('CGLinearSolver', name="linear solver", iterations="25", tolerance="1e-10", threshold="10e-10")
        instrumentNode.createObject('MechanicalObject', name="mechObject", template="Rigid3d", 
                                                        dx = 0, dy = 6,  dz = 12,rx = 0, ry = 180, rz = 0, 
                                                        scale3d=[scale, scale, scale])
        instrumentNode.createObject('UniformMass', name="mass", totalMass="5")
        instrumentNode.createObject('UncoupledConstraintCorrection')

        # Vis node
        instrumentVisNode = instrumentNode.createChild("VisualModel")
        instrumentVisNode.createObject('MeshObjLoader', name='instrumentMeshLoader', filename=meshFile)
        instrumentVisNode.createObject('OglModel', name="InstrumentVisualModel", src='@instrumentMeshLoader', 
                                                   dy = -2*scale,  scale3d=[scale, scale, scale])
 
        instrumentVisNode.createObject('RigidMapping', name="MM-VM mapping", input="@../mechObject", output="@InstrumentVisualModel")

        # Collision node
        instrumentSurfNode = instrumentNode.createChild("CollisionModel")
        instrumentSurfNode.createObject('MeshObjLoader', filename=meshFile, name="loader")
        instrumentSurfNode.createObject('MeshTopology', src="@loader", name="InstrumentCollisionModel")
        instrumentSurfNode.createObject('MechanicalObject', src="@InstrumentCollisionModel", name="instrumentCollisionState",
                                                            dy = -2*scale, scale3d=[scale, scale, scale])
        instrumentSurfNode.createObject('LineCollisionModel', name="instrumentLine")
        instrumentSurfNode.createObject('PointCollisionModel', name="instrumentPoint")
        instrumentSurfNode.createObject('RigidMapping', name="MM-CM mapping", input="@../mechObject", output="@instrumentCollisionState")
        
        instrumentNode.createObject('LinearMovementConstraint', template="Rigid3d",
                             indices = 0,
                             keyTimes=[0, 0.8, 1.6, 1.7],
                             movements= [[0, 0, 0, 0, 0, 0],
                                         [0, 0,-3, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0]])
        return 0

def createScene(rootNode):
    obj = MainScene(rootNode)
    obj.createGraph(rootNode)