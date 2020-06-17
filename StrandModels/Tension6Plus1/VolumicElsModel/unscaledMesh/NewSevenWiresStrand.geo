Merge "NewSevenWiresStrand.step";
// Mesh.ScalingFactor=0.001; //FreeCAD works in mm. But to simplify dealing with units, we scale everything back to meters!
Physical Surface("FaceFixed") = {12, 9, 6, 3, 15, 18, 21};
//+
Physical Surface("FacePulled") = {7, 4, 10, 2, 13, 16, 19};
//+
Physical Volume("WireVol") = {2, 1, 3, 4, 5, 6, 7};
Mesh.SubdivisionAlgorithm=2; // All hexa
// We can activate the calculation of mesh element sizes based on curvature:
Mesh.CharacteristicLengthFromCurvature = 1;
k=2;
Mesh.MinimumElementsPerTwoPi = 10;
Mesh.CharacteristicLengthMin = k * 1;
Mesh.CharacteristicLengthMax = k* 5;
Mesh.Algorithm=1;//adapted for curved geometry
//Mesh.SaveAll = 0;
//RecombineMesh;
//Mesh 2;//Does not work without it
//Mesh 2;//Does not work without it
//Mesh.Recombine3DLevel=0;//for quads

//uncomment if in GUI 
// Mesh.SurfaceEdges=0;
// Mesh 3;
//Mesh.VolumeFaces=1;//To show the mesh directly
// RefineMesh;
