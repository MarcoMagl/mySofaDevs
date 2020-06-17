#!/bin/bash
declare -a meshFiles #empty list
useTets=1
for i in 1
do
   res=$(echo print 1/$i. | python2)
   if [ "$useTets" = "1" ]; then
      meshFile="SevenWiresStrand2Lays${i}tets.msh"
   else
      meshFile="SevenWiresStrand2Lays${i}hex.msh"
   fi
   echo "The mesh file used is $meshFile"
   # meshFiles+=($meshFile)
   # #mesh the geometry
   gmsh SevenWiresStrandWtInput.geo -3 -setnumber useTets $useTets -setnumber stepFile SevenWiresStrand2Lays.step -o $meshFile -format msh2
   # # #run the simulation with the meshfile just created
   ~/Software/sofa/build/v19.12/bin/runSofa StrandJiangGeometry.py -n 1000000 -g batch --start --argv $meshFile $useTets
done
echo "Post processing start"
echo ${meshFiles[@]}
python2.7 PostProcessJiangGeometry.py ${meshFiles[@]}
echo "Post processing done"
