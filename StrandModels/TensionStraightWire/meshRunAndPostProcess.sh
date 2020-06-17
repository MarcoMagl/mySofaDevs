#!/bin/bash
declare -a meshFiles 
meshFile="SingleStraightWire1.msh"
meshFiles+=($meshFile)
#mesh the geometry
gmsh straightCylinderCircularSection.geo -o SingleStraightWire1.msh -format msh2 -3
#run the simulation with the meshfile just created
~/Software/sofa/build/v19.12/bin/runSofa pullOnSingleStraightWire.py -n 10000 -g batch --start --argv $meshFile
echo "Post processing start"
echo ${meshFiles[@]}
python2.7 PostProcessSingleStraightWire.py ${meshFiles[@]}
echo "Post processing done"
