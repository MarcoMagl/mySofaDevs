Merge "cylinder.step";
Physical Surface("FacePulled") = {3};
//+
Physical Surface("FaceFixed") = {2};
//+
Physical Volume("cyl") = {1};

// We can activate the calculation of mesh element sizes based on curvature:
Mesh.CharacteristicLengthFromCurvature = 1;
Mesh.MinimumElementsPerTwoPi = 10;

// We can constraint the min and max element sizes to stay within reasonnable
// values (see `t10.geo' for more details):
Mesh.CharacteristicLengthMin = 1;
Mesh.CharacteristicLengthMax = 5;
