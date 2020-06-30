Merge "SingleStraightWire.step";
Mesh.ScalingFactor=0.001; //FreeCAD works in mm. But to simplify dealing with units, we scale everything back to meters!
useTets=1;
If (useTets == 0)
    Mesh.SubdivisionAlgorithm=2; // All hexa
EndIf
// We can activate the calculation of mesh element sizes based on curvature:
Mesh.CharacteristicLengthFromCurvature = 1;
k=3;
Mesh.MinimumElementsPerTwoPi = k * 20;
Mesh.CharacteristicLengthMin = 2;
Mesh.CharacteristicLengthMax = 5;
Mesh.Algorithm=1;//adapted for curved geometry

//uncomment if in GUI 
// Mesh.SurfaceEdges=0;
// Mesh 3;
//Mesh.VolumeFaces=1;//To show the mesh directly
//Mesh 3;
RefineMesh;

