Merge "straightCylinderCircularSection.step";
Physical Surface("FaceBlocked") = {3};
//+
Physical Surface("FacePulled") = {2};
//+
Physical Volume("Cyl") = {1};
Mesh.CharacteristicLengthFromCurvature = 1;
k=2;
Mesh.MinimumElementsPerTwoPi = 10;
Mesh.CharacteristicLengthMin = k * 1;
Mesh.CharacteristicLengthMax = k* 5;

