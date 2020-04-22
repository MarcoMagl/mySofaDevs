#ifndef ACEGENCONTACTROUTINES_H
#define ACEGENCONTACTROUTINES_H 

#include "AceGenSources/sms.h"
#include "CurveToCurve2NodedBeams.cpp"

void CurveToCurve2NodedBeams(double X[4][3]
     ,double u[4][3],double (*kN),double (*radiusBI),double (*radiusBJ),double (*T)
     ,double (*gN),double h[2],double R[12],double K[12][12],int (*ExitCode),int 
     (*CubicPenaltyPotential));

#endif