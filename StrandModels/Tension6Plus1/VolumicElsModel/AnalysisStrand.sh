#!/bin/bash
~/Software/sofa/build/v19.12/bin/runSofa StrandJiangGeometry.py -n 10000 -g batch --start
python2.7 PostProcessJiangGeometry.py 
xdg-open epsilonVSAxialLoad.png
xdg-open timeVSepsilon.png


