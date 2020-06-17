Merge "SevenWiresStrand.step";
Mesh.ScalingFactor=0.001; //FreeCAD works in mm. But to simplify dealing with units, we scale everything back to meters!
Physical Surface("FacePulled") = {12, 9, 6, 3, 15, 18, 21};
//+
Physical Surface("FaceFixed") = {7, 4, 10, 2, 13, 16, 19};
//+
Physical Volume("WireVol") = {2, 1, 3, 4, 5, 6, 7};
If (useTets == 0)
    Mesh.SubdivisionAlgorithm=2; // All hexa
EndIf
// We can activate the calculation of mesh element sizes based on curvature:
Mesh.CharacteristicLengthFromCurvature = 1;
k=2;
Mesh.MinimumElementsPerTwoPi = 10;
Mesh.CharacteristicLengthMin = k * 1;
Mesh.CharacteristicLengthMax = k* 5;
Mesh.Algorithm=1;//adapted for curved geometry

//uncomment if in GUI 
// Mesh.SurfaceEdges=0;
// Mesh 3;
//Mesh.VolumeFaces=1;//To show the mesh directly
// RefineMesh;