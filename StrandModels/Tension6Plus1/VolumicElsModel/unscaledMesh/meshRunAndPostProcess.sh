#!/bin/bash
declare -a meshFiles #empty list
useTets=0
for i in 1
do
   res=$(echo print 1/$i. | python2)
   if [ "$useTets" = "1" ]; then
      meshFile="NewSevenWiresStrand${i}tets.msh"
   else
      meshFile="NewSevenWiresStrand${i}hex.msh"
   fi
   echo "The mesh file used is $meshFile"
   meshFiles+=($meshFile)
   #mesh the geometry
   # gmsh NewSevenWiresStrand.geo -setnumber useTets $useTets -3 -o $meshFile -format msh2
   gmsh NewSevenWiresStrand.geo -3 -o $meshFile -format msh2
   # #run the simulation with the meshfile just created
   ~/Software/sofa/build/v19.12/bin/runSofa StrandJiangGeometry.py -n 1000000 -g batch --start --argv $meshFile $useTets
done
echo "Post processing start"
echo ${meshFiles[@]}
python2.7 PostProcessJiangGeometry.py ${meshFiles[@]}
echo "Post processing done"
